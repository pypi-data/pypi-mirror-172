import asyncio
import json
import logging
import platform
import re
import sys
import typing
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from contextlib import asynccontextmanager
from hashlib import md5
from logging import getLogger
from os import environ
from pathlib import Path
from tempfile import TemporaryDirectory
from threading import Lock
from typing import BinaryIO, Dict, Iterable, Optional, Set, Union

import aiohttp
import backoff
import pkg_resources
from dask import config
from importlib_metadata import Distribution, distributions
from packaging import specifiers, version
from packaging.tags import Tag
from packaging.utils import parse_wheel_filename
from typing_extensions import Literal, TypedDict

logger = getLogger("coiled.package_sync")
subdir_datas = {}
PYTHON_VERSION = platform.python_version_tuple()


class PackageInfo(TypedDict):
    name: str
    source: Literal["pip", "conda"]
    channel: Optional[str]
    conda_name: Optional[str]
    client_version: str
    specifier: str
    include: bool
    issue: Optional[str]
    sdist: Optional[BinaryIO]


class PackageLevel(TypedDict):
    name: str
    level: int


class SpecifierStrict:
    # hacky workaround for conda versions not
    # sticking to PEP440
    # eg packaging turns 2022c into 2022rc0 otherwise
    def __init__(self, specifier: str):
        self.specifier = specifier

    def __contains__(self, item: str):
        return self.specifier == item

    def __str__(self):
        return f"=={self.specifier}"


SpecifierType = Union[specifiers.SpecifierSet, SpecifierStrict]


def create_specifier(v: str, priority: int) -> SpecifierType:
    # Note specifiers are created using the parsed version due to
    # https://github.com/pypa/packaging/issues/583
    if not len(v.split(".")) > 2:
        # return specifiers.SpecifierSet(f"==*")
        return SpecifierStrict(v)
    try:
        parsed_version = version.parse(v)
        if isinstance(parsed_version, version.LegacyVersion):
            return specifiers.SpecifierSet("==*")
        else:
            if priority >= 100:
                return specifiers.SpecifierSet(
                    f"=={parsed_version}",
                    prereleases=parsed_version.is_prerelease,
                )
            elif priority == -1:
                return specifiers.SpecifierSet("=*", parsed_version.is_prerelease)
            else:
                return specifiers.SpecifierSet(
                    f"~={parsed_version}",
                    prereleases=parsed_version.is_prerelease,
                )
    except (version.InvalidVersion, specifiers.InvalidSpecifier):
        return specifiers.SpecifierSet("==*")


def any_matches(versions: Iterable[str], specifier: SpecifierType):
    for available_version in versions:
        if specifier and available_version in specifier:
            return True
    else:
        return False


# private threadpool required to prevent deadlocks
# while waiting for a lock
_lockPool = ThreadPoolExecutor(max_workers=1)


@asynccontextmanager
async def async_thread_lock(lock: Lock):
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(_lockPool, lock.acquire)
    try:
        yield
    finally:
        lock.release()


class RepoCache:
    CACHE_DIR = Path(config.PATH) / "coiled-cache"

    channel_memory_cache: typing.DefaultDict[
        str, typing.DefaultDict[str, typing.Dict]
    ] = defaultdict(lambda: defaultdict(dict))

    lock = Lock()

    @backoff.on_exception(backoff.expo, aiohttp.ClientConnectionError, max_time=60)
    async def load_channel_repo_data(self, channel: str):
        logger.info(f"Loading conda metadata.json for {channel}")
        if not self.CACHE_DIR.exists():
            self.CACHE_DIR.mkdir(parents=True, exist_ok=True)
        channel_filename = Path(md5(channel.encode("utf-8")).hexdigest()).with_suffix(
            ".json"
        )
        channel_fp = self.CACHE_DIR / channel_filename
        headers = {}
        channel_cache_meta_fp = channel_fp.with_suffix(".meta_cache")
        if channel_cache_meta_fp.exists():
            with channel_cache_meta_fp.open("r") as cache_meta_f:
                channel_cache_meta = json.load(cache_meta_f)
            headers["If-None-Match"] = channel_cache_meta["etag"]
            headers["If-Modified-Since"] = channel_cache_meta["mod"]
        async with aiohttp.ClientSession() as client:
            resp = await client.get(channel + "/" + "repodata.json", headers=headers)
            if resp.status == 304:
                logger.info(f"Cached version is valid for {channel}, loading")
                data = json.loads(channel_fp.read_text())
            else:
                logger.info(f"Downloading fresh conda repodata for {channel}")
                data = await resp.json()
                channel_fp.write_text(json.dumps(data))
                channel_cache_meta_fp.write_text(
                    json.dumps(
                        {
                            "etag": resp.headers["Etag"],
                            "mod": resp.headers["Last-Modified"],
                        }
                    )
                )
            for pkg in data["packages"].values():
                self.channel_memory_cache[channel][pkg["name"]][pkg["version"]] = pkg

    async def fetch_repo_data(self, channel: str) -> typing.Dict[str, typing.Dict]:
        async with async_thread_lock(self.lock):
            # check again once we have the lock in case
            # someone beat us to it
            if not self.channel_memory_cache.get(channel):
                await self.load_channel_repo_data(channel)
                return self.channel_memory_cache[channel]
            else:
                return self.channel_memory_cache[channel]

    async def is_available(
        self,
        name: str,
        channel_url: str,
        specifier: SpecifierType,
    ) -> bool:
        repo_data = await self.fetch_repo_data(channel=channel_url + "/linux-64")
        if repo_data.get(name):
            return any_matches(versions=repo_data[name].keys(), specifier=specifier)
        else:
            return False


class CondaPackage:
    def __init__(self, meta_json: typing.Dict, prefix: Path):
        self.prefix = prefix
        self.name = meta_json["name"]
        self.version = meta_json["version"]
        self.subdir = meta_json["subdir"]
        self.files = meta_json["files"]
        channel_regex = rf"(.*\.\w*)/?(.*)/{self.subdir}$"
        result = re.match(channel_regex, meta_json["channel"])
        if not result:
            logger.debug(
                f"Channel {meta_json['channel']} does not match url pattern, falling"
                "back to https://conda.anaconda.org"
            )
            self.channel_url = f"https://conda.anaconda.org/{meta_json['channel']}"
            self.channel = meta_json["channel"]
        else:
            self.channel_url = result.group(1) + "/" + result.group(2)
            self.channel = result.group(2)


class CondaEnv:
    global_repo_cache = RepoCache()

    def __init__(
        self,
        priorities: Dict[str, int],
        only: Optional[Set[str]] = None,
        repo_cache: Optional[RepoCache] = None,
        strict: bool = False,
    ):
        self.strict = strict
        self.repo_cache = repo_cache or self.global_repo_cache
        self.priorities = priorities
        self.only = only
        conda_default_env = environ.get("CONDA_DEFAULT_ENV")
        self.conda_default_env = Path(conda_default_env) if conda_default_env else None
        conda_prefix = environ.get("CONDA_PREFIX")
        self.conda_prefix = Path(conda_prefix) if conda_prefix else None

    async def approximate(self) -> typing.Dict[str, PackageInfo]:
        if self.conda_default_env and self.conda_prefix:
            logger.info(f"Conda environment detected: {self.conda_default_env}")
            return await self.iterate_conda_packages()
        else:
            # User is not using conda, we should just grab their python version
            # so we know what to install
            return await self.default_python_env()

    async def default_python_env(self) -> typing.Dict[str, PackageInfo]:
        python_version = platform.python_version()
        specifier = specifiers.SpecifierSet(f"=={python_version}")
        python_pkg: PackageInfo = {
            "name": "python",
            "source": "conda",
            "sdist": None,
            "conda_name": "python",
            "client_version": python_version,
            "specifier": str(specifier),
            "include": True,
            "channel": "conda-forge",
            "issue": None,
        }
        if not await self.repo_cache.is_available(
            name="python",
            channel_url="https://conda.anaconda.org/conda-forge",
            specifier=specifier,
        ):
            python_pkg["include"] = False
            python_pkg[
                "issue"
            ] = "Only python versions available on conda-forge are supported"

        return {"python": python_pkg}

    async def iterate_conda_packages(
        self,
    ) -> Dict[str, PackageInfo]:
        assert self.conda_prefix
        conda_meta = self.conda_prefix / "conda-meta"

        if conda_meta.exists() and conda_meta.is_dir():
            conda_packages = [
                CondaPackage(json.load(metafile.open("r")), prefix=self.conda_prefix)
                for metafile in conda_meta.iterdir()
                if metafile.suffix == ".json"
            ]
            if self.only:
                conda_packages = filter(
                    lambda pkg: pkg.name in self.only, conda_packages
                )
            packages = await asyncio.gather(
                *[self.handle_conda_package(pkg) for pkg in conda_packages]
            )
            return {pkg["name"]: pkg for pkg in packages}
        else:
            return {}

    async def handle_conda_package(self, pkg: CondaPackage) -> PackageInfo:
        # Are there conda packages that install multiple python packages?
        metadata_location = next(
            (Path(fp).parent for fp in pkg.files if re.match(r".*/METADATA$", fp)), None
        )
        if metadata_location:
            dist = Distribution.at(pkg.prefix / metadata_location)
            name = dist.metadata["Name"] or pkg.name
        else:
            name = pkg.name
        return await self.create_conda_package_info(name=name, pkg=pkg)

    async def create_conda_package_info(
        self, name: str, pkg: CondaPackage
    ) -> PackageInfo:
        # strict mode overrides all priorities
        priority = 100 if self.strict else self.priorities.get(name.lower(), 50)
        if priority == -2:
            return {
                "channel": pkg.channel,
                "sdist": None,
                "source": "conda",
                "conda_name": pkg.name,
                "name": name or pkg.name,
                "client_version": pkg.version,
                "specifier": "",
                "include": False,
                "issue": "Package ignored",
            }
        specifier = create_specifier(pkg.version, priority=priority)
        package_info: PackageInfo = {
            "channel": pkg.channel,
            "sdist": None,
            "source": "conda",
            "conda_name": pkg.name,
            "name": name or pkg.name,
            "client_version": pkg.version,
            "specifier": str(specifier),
            "include": True,
            "issue": None,
        }
        if pkg.subdir != "noarch" and not await self.repo_cache.is_available(
            name=pkg.name, channel_url=pkg.channel_url, specifier=specifier
        ):
            package_info["include"] = False
            package_info[
                "issue"
            ] = f"{pkg.version} has no install candidate for linux-64"
        return package_info


class PipRepo:
    def __init__(self, client: aiohttp.ClientSession):
        self.client = client
        self.looking_for = [
            Tag(f"py{PYTHON_VERSION[0]}", "none", "any"),
            Tag(f"cp{PYTHON_VERSION[0]}{PYTHON_VERSION[1]}", "none", "any"),
        ]

    @backoff.on_exception(backoff.expo, aiohttp.ClientConnectionError, max_time=60)
    async def fetch(self, package_name):
        resp = await self.client.get(f"/pypi/{package_name}/json")
        data = await resp.json()
        pkgs = {}
        for build_version, builds in data["releases"].items():
            for build in [
                b
                for b in builds
                if not b.get("yanked")
                and b["packagetype"] not in ["bdist_dumb", "bdist_wininst", "bdist_rpm"]
            ]:
                if build["packagetype"] == "bdist_wheel":
                    _, _, _, tags = parse_wheel_filename(build["filename"])
                elif build["packagetype"] == "sdist":
                    tags = [
                        Tag(f"py{PYTHON_VERSION[0]}", "none", "any"),
                    ]
                else:
                    dist = pkg_resources.Distribution.from_filename(build["filename"])
                    tags = [Tag(f"py{dist.py_version}", "none", "any")]
                if any(valid in tags for valid in self.looking_for):
                    pkgs[build_version] = build
        return pkgs


class PackageBuildError(Exception):
    pass


class CondaPlaceHolder(dict):
    pass


async def create_wheel(pkg_name: str, version: str, src: str) -> PackageInfo:
    tmpdir = TemporaryDirectory()
    outdir = Path(tmpdir.name) / Path(pkg_name)
    logger.info(f"Attempting to create a wheel for {pkg_name} in directory {src}")
    p = await asyncio.create_subprocess_shell(
        cmd=f"pip wheel --wheel-dir {outdir} --no-deps --no-binary :all: {src}"
    )
    await p.wait()
    if p.returncode:
        return {
            "name": pkg_name,
            "source": "pip",
            "channel": None,
            "conda_name": None,
            "client_version": version,
            "specifier": "",
            "include": False,
            "issue": (
                "Failed to build a wheel for the"
                " package, will not be included in environment, check stdout for details"
            ),
            "sdist": None,
        }
    wheel_fn = next(file for file in outdir.iterdir() if file.suffix == ".whl")
    return {
        "name": pkg_name,
        "source": "pip",
        "channel": None,
        "conda_name": None,
        "client_version": version,
        "specifier": "",
        "include": True,
        "issue": f"Wheel built from {src}",
        "sdist": wheel_fn.open("rb"),
    }


async def create_wheel_from_egg(pkg_name: str, version: str, src: str) -> PackageInfo:
    tmpdir = TemporaryDirectory()
    outdir = Path(tmpdir.name) / Path(pkg_name)
    outdir.mkdir(parents=True)
    logger.info(f"Attempting to create a wheel for {pkg_name} in directory {src}")
    p = await asyncio.create_subprocess_shell(
        cmd=f"wheel convert --dest-dir {outdir} {src}"
    )
    await p.wait()
    if p.returncode:
        return {
            "name": pkg_name,
            "source": "pip",
            "channel": None,
            "conda_name": None,
            "client_version": version,
            "specifier": "",
            "include": False,
            "issue": (
                "Failed to build a wheel for the"
                " package, will not be included in environment, check stdout for details"
            ),
            "sdist": None,
        }
    wheel_fn = next(file for file in outdir.iterdir() if file.suffix == ".whl")
    return {
        "name": pkg_name,
        "source": "pip",
        "channel": None,
        "conda_name": None,
        "client_version": version,
        "specifier": "",
        "include": True,
        "issue": "Wheel built from local egg",
        "sdist": wheel_fn.open("rb"),
    }


async def handle_standard_dist(
    dist: Distribution, priority: int, repo: PipRepo
) -> PackageInfo:
    specifier = create_specifier(dist.version, priority=priority)
    data = await repo.fetch(dist.name)
    if not any_matches(versions=data.keys(), specifier=specifier):
        return {
            "name": dist.name,
            "source": "pip",
            "conda_name": None,
            "channel": None,
            "client_version": dist.version,
            "specifier": str(specifier),
            "include": False,
            "issue": f"Cannot find {dist.name}{specifier} on pypi",
            "sdist": None,
        }

    return {
        "name": dist.name,
        "source": "pip",
        "channel": None,
        "conda_name": None,
        "client_version": dist.version,
        "specifier": str(specifier),
        "include": True,
        "issue": None,
        "sdist": None,
    }


async def handle_dist(
    dist: Distribution, repo: PipRepo, priorities: Dict[str, int], strict: bool = False
) -> Optional[Union[PackageInfo, CondaPlaceHolder]]:
    installer = dist.read_text("INSTALLER")
    if not dist.name:
        return {
            "name": str(dist._path),  # type: ignore
            "source": "pip",
            "channel": None,
            "conda_name": None,
            "client_version": dist.version,
            "specifier": "",
            "include": False,
            "issue": "Package has no recognizable name and has been omitted",
            "sdist": None,
        }
    priority = 100 if strict else priorities.get(dist.name.lower(), 50)
    if priority == -2:
        return {
            "name": dist.name,
            "source": "pip",
            "channel": None,
            "conda_name": None,
            "client_version": dist.version,
            "specifier": "",
            "include": False,
            "issue": "Package ignored",
            "sdist": None,
        }
    elif installer and installer.rstrip() == "conda":
        return CondaPlaceHolder(name=dist.name)
    elif dist._path.parent.suffix == ".egg":  # type: ignore
        return await create_wheel_from_egg(
            pkg_name=dist.name,
            version=dist.version,
            src=dist._path.parent,  # type: ignore
        )
    elif dist._path.suffix == ".egg-info":  # type: ignore
        return CondaPlaceHolder(name=dist.name)
    else:
        direct_url_metadata = dist.read_text("direct_url.json")
        if direct_url_metadata:
            url_metadata = json.loads(direct_url_metadata)
            if url_metadata.get("vcs_info"):
                vcs_info = url_metadata.get("vcs_info")
                vcs = vcs_info["vcs"]
                commit = vcs_info["commit_id"]
                url = url_metadata["url"]
                if vcs == "git":
                    # TODO: Download source + build sdist?
                    # this would allow private repos to work well
                    pip_url = f"git+{url}@{commit}"
                    return await create_wheel(
                        pkg_name=dist.name, version=dist.version, src=pip_url
                    )
            elif url_metadata.get("dir_info", {}).get("editable"):
                return await create_wheel(
                    pkg_name=dist.name,
                    version=dist.version,
                    src=url_metadata["url"],
                )
        potential_egg_link_name = Path(dist.name).with_suffix(".egg-link")
        egg_links = [
            Path(location)
            for location in sys.path
            if (Path(location) / potential_egg_link_name).is_file()
        ]
        if egg_links:
            return await create_wheel(
                pkg_name=dist.name,
                version=dist.version,
                src=dist._path.parent,  # type:ignore
            )
        else:
            return await handle_standard_dist(dist, priority, repo)


async def create_pip_env_approximation(
    priorities: Dict[str, int],
    only: Optional[Set[str]] = None,
    strict: bool = False,
) -> typing.Dict[str, Union[PackageInfo, CondaPlaceHolder]]:
    async with aiohttp.ClientSession("https://pypi.org") as client:
        # distributions returns ALL distributions
        # even ones that are not active
        # this is a trick so we only get the distribution
        # that is last in stack
        active_dists: Dict[str, Distribution] = {
            dist.name: dist for dist in distributions()
        }
        dists = active_dists.values()
        pip_repo = PipRepo(client=client)
        if only:
            dists = filter(lambda pkg: pkg.name in only, dists)  # type: ignore
        return {
            pkg["name"]: pkg
            for pkg in await asyncio.gather(
                *(
                    handle_dist(
                        dist, repo=pip_repo, priorities=priorities, strict=strict
                    )
                    for dist in dists
                )
            )
            if pkg
        }


async def create_environment_approximation(
    priorities: Dict[str, int], only: Optional[Set[str]] = None, strict: bool = False
) -> typing.List[PackageInfo]:
    # TODO: private conda channels
    # TODO: detect pre-releases and only set --pre flag for those packages (for conda)
    conda_env = CondaEnv(priorities=priorities, only=only, strict=strict)
    conda_env_future = asyncio.create_task(conda_env.approximate())
    pip_env_future = asyncio.create_task(
        create_pip_env_approximation(only=only, priorities=priorities, strict=strict)
    )
    conda_env = await conda_env_future
    pip_env = await pip_env_future
    filterd_conda = {}
    # the pip list is the "truth" of what is imported for python deps
    for name, package in conda_env.items():
        # if a package exists in the pip list but is not a conda place holder
        # then the conda package wont be imported and should be discarded
        if pip_env.get(name):
            if isinstance(pip_env[name], CondaPlaceHolder):
                filterd_conda[name] = package
        else:
            # a non python package and safe to include
            filterd_conda[name] = package
    # remove conda placeholders
    pip_env = {
        pkg_name: pkg
        for pkg_name, pkg in pip_env.items()
        if not isinstance(pkg, CondaPlaceHolder)
    }
    return list(pip_env.values()) + list(conda_env.values())


if __name__ == "__main__":
    from logging import basicConfig

    basicConfig(level=logging.INFO)
    import pprint

    result = asyncio.run(
        create_environment_approximation(priorities={"dask": 100, "twisted": -2})
    )
    pprint.pprint(result)
