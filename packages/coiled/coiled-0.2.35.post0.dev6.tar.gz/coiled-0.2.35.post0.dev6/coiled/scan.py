import asyncio
import json
import logging
import os
import platform
import re
import sys
import typing
from logging import getLogger
from pathlib import Path
from typing import Dict, List, Optional, Union

from importlib_metadata import Distribution

from .types import CondaPackage, CondaPlaceHolder, PackageInfo

logger = getLogger("coiled.package_sync")
subdir_datas = {}
PYTHON_VERSION = platform.python_version_tuple()


async def scan_conda(prefix: Path) -> typing.Dict[str, PackageInfo]:
    conda_meta = prefix / "conda-meta"
    if conda_meta.exists() and conda_meta.is_dir():
        conda_packages = [
            CondaPackage(json.load(metafile.open("r")), prefix=prefix)
            for metafile in conda_meta.iterdir()
            if metafile.suffix == ".json"
        ]
        packages = await asyncio.gather(
            *[handle_conda_package(pkg) for pkg in conda_packages]
        )
        return {pkg["name"]: pkg for pkg in packages}
    else:
        return {}


async def handle_conda_package(pkg: CondaPackage) -> PackageInfo:
    # Are there conda packages that install multiple python packages?
    metadata_location = next(
        (Path(fp).parent for fp in pkg.files if re.match(r".*/METADATA$", fp)), None
    )
    if metadata_location:
        dist = Distribution.at(pkg.prefix / metadata_location)
        name = dist.metadata["Name"] or pkg.name
    else:
        name = pkg.name
    return {
        "channel": pkg.channel,
        "channel_url": pkg.channel_url,
        "source": "conda",
        "conda_name": pkg.name,
        "subdir": pkg.subdir,
        "name": name or pkg.name,
        "version": pkg.version,
        "wheel_target": None,
    }


async def handle_dist(
    dist: Distribution, prefix: Path
) -> Optional[Union[PackageInfo, CondaPlaceHolder]]:
    installer = dist.read_text("INSTALLER") or ""
    installer = installer.rstrip()
    if installer == "conda":
        return CondaPlaceHolder(name=dist.name)
    elif dist._path.parent.suffix == ".egg":  # type: ignore
        return {
            "name": dist.name,
            "source": "pip",
            "channel": None,
            "channel_url": None,
            "conda_name": None,
            "version": dist.version,
            "wheel_target": str(dist._path.parent),  # type: ignore
        }
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
                    return {
                        "name": dist.name,
                        "source": "pip",
                        "channel": None,
                        "channel_url": None,
                        "subdir": None,
                        "conda_name": None,
                        "version": dist.version,
                        "wheel_target": pip_url,
                    }
            elif url_metadata.get("url"):
                return {
                    "name": dist.name,
                    "source": "pip",
                    "channel": None,
                    "channel_url": None,
                    "subdir": None,
                    "conda_name": None,
                    "version": dist.version,
                    "wheel_target": url_metadata["url"],
                }
        if os.name == "nt":
            potential_egg_link_name = (
                prefix
                / "lib"
                / "site-packages"
                / Path(dist.name).with_suffix(".egg-link")
            )
        else:
            python = prefix / "bin" / "python"
            potential_egg_link_name = (
                prefix
                / getattr(sys, "platlibdir", "lib")
                / python.resolve().name
                / "site-packages"
                / Path(dist.name).with_suffix(".egg-link")
            )
        if potential_egg_link_name.is_file():
            return {
                "name": dist.name,
                "source": "pip",
                "channel": None,
                "channel_url": None,
                "subdir": None,
                "conda_name": None,
                "version": dist.version,
                "wheel_target": str(dist._path.parent),  # type: ignore
            }
        return {
            "name": dist.name,
            "source": "pip",
            "channel": None,
            "channel_url": None,
            "subdir": None,
            "conda_name": None,
            "version": dist.version,
            "wheel_target": None,
        }


async def scan_pip(
    prefix: Path,
) -> typing.Dict[str, Union[PackageInfo, CondaPlaceHolder]]:
    # distributions returns ALL distributions
    # even ones that are not active
    # this is a trick so we only get the distribution
    # that is last in stack
    if os.name == "nt":
        site_packages = Path(prefix) / "lib" / "site-packages"
    else:
        python = (Path(prefix) / "bin" / "python").resolve().name
        site_packages = (
            Path(prefix) / getattr(sys, "platlibdir", "lib") / python / "site-packages"
        )
    paths: List[str] = [str(site_packages)]
    for fp in site_packages.iterdir():
        if fp.suffix in [".pth", ".egg-link"]:
            for line in fp.read_text().split("\n"):
                if line.startswith("#"):
                    continue
                elif line.startswith(("import", "import\t")):
                    continue
                elif line.rstrip() == ".":
                    continue
                else:
                    p = site_packages / Path(line.rstrip())
                    full_path = str(p.resolve())
                    if p.exists() and full_path not in paths:
                        paths.append(full_path)
    active_dists: Dict[str, Distribution] = {
        dist.name: dist for dist in Distribution.discover(path=list(paths))
    }
    dists = active_dists.values()
    return {
        pkg["name"]: pkg
        for pkg in await asyncio.gather(*(handle_dist(dist, prefix) for dist in dists))
        if pkg
    }


async def scan_prefix(prefix: Optional[Path] = None) -> typing.List[PackageInfo]:
    # TODO: private conda channels
    # TODO: detect pre-releases and only set --pre flag for those packages (for conda)
    if not prefix:
        prefix = Path(sys.prefix)
    conda_env_future = asyncio.create_task(scan_conda(prefix=prefix))
    pip_env_future = asyncio.create_task(scan_pip(prefix=prefix))
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
            elif pip_env[name]["version"] == package["version"]:
                pip_env.pop(name, None)
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
    return sorted(
        list(pip_env.values()) + list(filterd_conda.values()),
        key=lambda pkg: pkg["name"],
    )


if __name__ == "__main__":
    import sys
    from logging import basicConfig

    from rich.console import Console
    from rich.table import Table

    basicConfig(level=logging.INFO)

    result = asyncio.run(scan_prefix(Path(sys.prefix)))
    table = Table(title="Packages")
    table.add_column("Package Name", style="cyan", no_wrap=True)
    table.add_column("Version", style="magenta")
    table.add_column("Source", style="magenta")
    table.add_column("Path", style="green")

    for pkg in result:
        table.add_row(
            pkg["name"], pkg["version"], pkg["source"], str(pkg["wheel_target"] or "")
        )
    console = Console()
    console.print(table)
