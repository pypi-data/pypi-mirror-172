import os
import pytest
from ..data import bliss


def test_find_lima_files(bliss_scan):
    expected = [
        os.path.join(bliss_scan.dirname, "scan0002", f"p3_{i}.h5") for i in range(11)
    ]
    found = bliss._find_lima_files(bliss_scan, 2, "p3")
    assert expected == found
    assert not bliss._find_lima_files(bliss_scan, 1, "p3")
    assert not bliss._find_lima_files(bliss_scan, 2, "p")


def test_iter_lima_blocks(bliss_scan):
    filenames = bliss._find_lima_files(bliss_scan, 2, "p3")
    file_fmt = os.path.join(bliss_scan.dirname, "scan0002", "p3_{}.h5")
    dset_path = "/entry_0000/measurement/data"

    expected = [(file_fmt.format(i), dset_path, 0, 3) for i in range(11)]
    found = list(bliss._iter_lima_blocks(filenames))
    assert expected == found

    expected = [(file_fmt.format(0), dset_path, 0, 1)]
    found = list(bliss._iter_lima_blocks(filenames, start_index=0, end_index=1))
    assert expected == found

    expected = [
        (file_fmt.format(0), dset_path, 2, 3),
        (file_fmt.format(1), dset_path, 0, 1),
    ]
    found = list(bliss._iter_lima_blocks(filenames, start_index=2, end_index=4))
    assert expected == found

    expected = [
        (file_fmt.format(2), dset_path, 2, 3),
        (file_fmt.format(3), dset_path, 0, 1),
    ]
    found = list(
        bliss._iter_lima_blocks(filenames, start_index=2 + 2 * 3, end_index=4 + 2 * 3)
    )
    assert expected == found

    expected = [(file_fmt.format(i), dset_path, 0, 3) for i in range(2, 11)]
    found = list(bliss._iter_lima_blocks(filenames, start_index=2 * 3))
    assert expected == found


@pytest.mark.parametrize("lima_names", [(), ("p3",), ("p3", "p4")])
@pytest.mark.parametrize("counter_names", [(), ("diode1",), ("diode1", "diode2")])
def test_iter_bliss_data(lima_names, counter_names, bliss_scan):
    nexpected = len(lima_names) + len(counter_names)
    index = None
    for (index, data,) in bliss.iter_bliss_data(
        bliss_scan, 2, lima_names=lima_names, counter_names=counter_names
    ):
        assert len(data) == nexpected
        if "diode1" in counter_names:
            assert data["diode1"] == index
        if "diode2" in counter_names:
            assert data["diode2"] == index
        if "p3" in counter_names:
            assert (data["p3"] == index).all()
        if "p4" in counter_names:
            assert (data["p4"] == index).all()

    if nexpected:
        # Lima saved more images than scan points (32 instead of 30)
        if counter_names:
            assert index == 30
        else:
            assert index == 32
    else:
        assert index is None
