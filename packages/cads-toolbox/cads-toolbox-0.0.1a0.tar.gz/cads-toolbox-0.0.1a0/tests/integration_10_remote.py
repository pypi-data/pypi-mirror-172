import os
import pathlib
from typing import Any, Dict, Tuple

import cacholote
import pytest

import cads_toolbox


@pytest.fixture
def request_args() -> Tuple[str, Dict[str, Any]]:
    return (
        "reanalysis-era5-single-levels",
        {
            "variable": "2m_temperature",
            "product_type": "reanalysis",
            "year": "2017",
            "month": "01",
            "day": "01",
            "time": "12:00",
        },
    )


def test_uncached_download(
    tmpdir: pathlib.Path, request_args: Tuple[str, Dict[str, Any]]
):
    cads_toolbox.config.USE_CACHE = False

    remote = cads_toolbox.catalogue.retrieve(*request_args)
    target = str(tmpdir / "test.grib")

    # Download
    assert remote.download(target) == target
    assert os.path.getsize(target) == 2076600

    # Re-download
    previous_mtime = os.path.getmtime(target)
    assert remote.download(target) == target
    assert os.path.getmtime(target) != previous_mtime
    assert os.path.getsize(target) == 2076600


def test_cached_download(
    tmpdir: pathlib.Path, request_args: Tuple[str, Dict[str, Any]]
):
    cads_toolbox.config.USE_CACHE = True

    remote = cads_toolbox.catalogue.retrieve(*request_args)
    with cacholote.config.set(cache_store_directory=tmpdir):
        # Download to cache
        cache_file = remote.download()
        assert os.path.getsize(cache_file) == 2076600
        assert os.path.dirname(cache_file) == tmpdir

        # Use cached file
        previous_mtime = os.path.getmtime(cache_file)
        assert remote.download() == cache_file
        assert os.path.getmtime(cache_file) == previous_mtime

        # Copy from cache file
        target = str(tmpdir / "test.grib")
        assert remote.download(target=target) == target
        assert os.path.getsize(target) == 2076600
        assert os.path.getmtime(cache_file) == previous_mtime


def test_to_xarray(tmpdir: pathlib.Path, request_args: Tuple[str, Dict[str, Any]]):
    xr = pytest.importorskip("xarray")

    cads_toolbox.config.USE_CACHE = True
    remote = cads_toolbox.catalogue.retrieve(*request_args)
    with cacholote.config.set(cache_store_directory=tmpdir):
        assert isinstance(remote.to_xarray(), xr.Dataset)


def test_to_pandas(tmpdir: pathlib.Path, request_args: Tuple[str, Dict[str, Any]]):
    pd = pytest.importorskip("pandas")

    cads_toolbox.config.USE_CACHE = True
    remote = cads_toolbox.catalogue.retrieve(*request_args)
    with cacholote.config.set(cache_store_directory=tmpdir):
        assert isinstance(remote.to_pandas(), pd.DataFrame)
