import asyncio
from pathlib import Path

from coiled.scan import scan_prefix


def test_scan():
    env = asyncio.run(scan_prefix(Path(__file__).parent / "dummy-env"))
    egg_link_pkg = next((pkg for pkg in env if pkg["name"] == "egg_link_package"))
    env.remove(egg_link_pkg)
    # wheel target will be system specific as it's a
    # full path
    wheel_target = egg_link_pkg["wheel_target"]
    del egg_link_pkg["wheel_target"]  # type: ignore
    assert isinstance(wheel_target, str)
    assert wheel_target.endswith(
        "python-api/coiled/tests/dummy-env/src/egg_link_package"
    )
    assert egg_link_pkg == {
        "channel": None,
        "channel_url": None,
        "conda_name": None,
        "name": "egg_link_package",
        "source": "pip",
        "subdir": None,
        "version": "0.0.5",
    }
    assert env == [
        {
            "channel": "conda-forge",
            "channel_url": "https://conda.anaconda.org/conda-forge",
            "conda_name": "condapythonpackage",
            "name": "conda_python_package_python_name",
            "source": "conda",
            "subdir": "noarch",
            "version": "0.1.0",
            "wheel_target": None,
        },
        {
            "channel": "conda-forge",
            "channel_url": "https://conda.anaconda.org/conda-forge",
            "conda_name": "condabinpackage",
            "name": "condabinpackage",
            "source": "conda",
            "subdir": "osx-arm64",
            "version": "0.0.2",
            "wheel_target": None,
        },
        {
            "channel": None,
            "channel_url": None,
            "conda_name": None,
            "name": "dist_info_git_package",
            "source": "pip",
            "subdir": None,
            "version": "0.0.10",
            "wheel_target": "git+https://github.com/dask/distributed.git@c2dfea237ffe802883b85617f20f7a7ad7b16080",
        },
        {
            "channel": None,
            "channel_url": None,
            "conda_name": None,
            "name": "dist_info_package",
            "source": "pip",
            "subdir": None,
            "version": "0.0.11",
            "wheel_target": None,
        },
        {
            "channel": None,
            "channel_url": None,
            "conda_name": None,
            "name": "egg_info_package",
            "source": "pip",
            "subdir": None,
            "version": "0.0.15",
            "wheel_target": None,
        },
        {
            "channel": None,
            "channel_url": None,
            "conda_name": None,
            "name": "poetry_package",
            "source": "pip",
            "subdir": None,
            "version": "0.0.11",
            "wheel_target": "file:///some/where/over/the/rainbow",
        },
        {
            "channel": None,
            "channel_url": None,
            "conda_name": None,
            "name": "pth_package",
            "source": "pip",
            "subdir": None,
            "version": "0.0.25",
            "wheel_target": "file:///some/where/over/the/rainbow",
        },
    ]
