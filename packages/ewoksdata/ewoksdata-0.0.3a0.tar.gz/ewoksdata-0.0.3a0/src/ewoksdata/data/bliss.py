import os
import re
from glob import glob
from numbers import Integral, Number
from typing import Iterator, List, Optional, Tuple, Sequence, Union

import numpy
import h5py
import hdf5plugin  # noqa F401
from numpy.typing import ArrayLike
from silx.io import h5py_utils
from silx.utils import retry as retrymod
from silx.io.utils import get_data as silx_get_data

from . import hdf5
from . import url


def get_data(
    data: Union[str, ArrayLike, Number], **options
) -> Union[numpy.ndarray, Number]:
    if isinstance(data, str):
        if data.endswith(".h5") or data.endswith(".nx"):
            filename, h5path, idx = url.h5dataset_url_parse(data)
            return get_hdf5_data(filename, h5path, idx=idx, **options)
        else:
            return silx_get_data(data)
    elif isinstance(data, (Sequence, Number, numpy.ndarray)):
        return data
    else:
        raise TypeError(type(data))


def get_image(*args, **kwargs) -> numpy.ndarray:
    data = get_data(*args, **kwargs)
    return numpy.atleast_2d(numpy.squeeze(data))


@h5py_utils.retry()
def get_hdf5_data(filename: str, h5path: str, idx=None, **options) -> numpy.ndarray:
    with hdf5.h5context(filename, h5path, **options) as dset:
        if _is_bliss_file(dset):
            if "end_time" not in hdf5.get_nxentry(dset):
                raise retrymod.RetryError
        if idx is None:
            idx = tuple()
        return dset[idx]


@h5py_utils.retry()
def iter_bliss_data(
    filename: str,
    scan_nr: Integral,
    lima_names: List[str],
    counter_names: List[str],
    start_index: Optional[Integral] = None,
    subscan: Optional[Integral] = None,
    **options,
) -> Iterator[Tuple[int, dict]]:
    """Iterate over the data from one Bliss scan. The counters are assumed to have
    many data values as scan points.

    :param str filename: the Bliss dataset filename
    :param Integral filename: the scan number in the dataset
    :param list lima_names: names of lima detectors
    :param list counter_names: names of non-lima detectors (you need to provide at least one)
    :param Integral start_index: start iterating from this scan point index
    :param Integral subscan: subscan number (for example "10.2" has `scan_nr=10` and `subscan=2`)
    :param Number retry_timeout: timeout when it cannot access the data for `retry_timeout` seconds
    :param Number retry_period: interval in seconds between data access retries
    :yields: scan index, data
    """
    if not subscan:
        subscan = 1
    if start_index is None:
        start_index = 0

    with hdf5.h5context(filename, f"{scan_nr}.{subscan}", **options) as scan:
        assert _is_bliss_file(scan), "Not a Bliss dataset file"
        measurement = scan["measurement"]
        finished = "end_time" in scan

        if counter_names:
            data = {name: measurement[name][start_index:] for name in counter_names}
            npoints = min(len(v) for v in data.values())
            if npoints == 0:
                if not finished:
                    raise retrymod.RetryError("not finished")
                return
        else:
            data = dict()

        lima_files = [
            _find_lima_files(filename, scan_nr, lima_name) for lima_name in lima_names
        ]
        if counter_names:
            end_index = start_index + npoints
            last_index = end_index - 1
        else:
            end_index = None
            last_index = None

        iterators = list(data.values())
        iterators.extend(
            _iter_lima_images(files, start_index, end_index) for files in lima_files
        )
        names = list(data) + list(lima_names)
        for i, ptdata in enumerate(zip(*iterators)):
            scan_index = start_index + i
            yield scan_index, dict(zip(names, ptdata))
            if last_index is not None and finished and scan_index == last_index:
                return

        if counter_names:
            raise retrymod.RetryError("not finished")
        else:
            if not finished:
                raise retrymod.RetryError("not finished")


def _find_lima_files(filename: str, scan_nr: Integral, lima_name: str) -> List[str]:
    lima_pattern = os.path.join(
        os.path.dirname(filename), f"scan*{scan_nr}/{lima_name}_*.h5"
    )
    lima_files = glob(lima_pattern)
    lima_nrs = [
        int(re.search(f"{lima_name}_([0-9]+).h5", os.path.basename(s)).group(1))
        for s in lima_files
    ]
    return [filename for _, filename in sorted(zip(lima_nrs, lima_files))]


def _iter_lima_images(
    lima_files: List[str],
    start_index: Optional[Integral] = None,
    end_index: Optional[Integral] = None,
    npoints_per_file: Optional[Integral] = None,
) -> Iterator[numpy.ndarray]:
    for (
        lima_file,
        lima_dset,
        slice_start_index,
        slice_end_index,
    ) in _iter_lima_blocks(lima_files, start_index, end_index, npoints_per_file):
        with hdf5.h5context(lima_file, lima_dset) as limadset:
            for lima_index in range(slice_start_index, slice_end_index):
                yield limadset[lima_index]


def _iter_lima_blocks(
    lima_files: List[str],
    start_index: Optional[Integral] = None,
    end_index: Optional[Integral] = None,
    npoints_per_file: Optional[Integral] = None,
) -> Iterator[Tuple[str, str, int, int]]:
    if not lima_files:
        return
    lima_dset = "/entry_0000/measurement/data"
    if npoints_per_file is None:
        with hdf5.h5context(lima_files[0]) as f:
            npoints_per_file = f[lima_dset].shape[0]

    if start_index is None:
        start_index = 0
    start_file_index = start_index // npoints_per_file
    if end_index is None:
        end_file_index = len(lima_files)
    else:
        end_file_index = (end_index - 1) // npoints_per_file + 1

    lima_files = lima_files[start_file_index:end_file_index]
    file_indices = list(range(start_file_index, end_file_index))
    for file_index, lima_file in zip(file_indices, lima_files):
        file_start_index = file_index * npoints_per_file
        file_end_index = file_start_index + npoints_per_file

        slice_start_index = max(file_start_index, start_index) - file_start_index
        if end_index is None:
            with hdf5.h5context(lima_file) as f:
                slice_end_index = f[lima_dset].shape[0]
        else:
            slice_end_index = min(file_end_index, end_index) - file_start_index
        yield lima_file, lima_dset, slice_start_index, slice_end_index


def _is_bliss_file(h5item: Union[h5py.Dataset, h5py.Group]) -> bool:
    return h5item.file.attrs.get("creator", "").lower() == "bliss"
