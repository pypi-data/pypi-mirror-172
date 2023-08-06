import h5py
import numpy
from ..data.hdf5.dataset_writer import DatasetWriter


def test_dataset_writer_variable_points(tmpdir):
    expected = list()
    filename = str(tmpdir / "test.h5")
    with h5py.File(filename, mode="w") as f:
        writer = DatasetWriter(f, "data")
        for _ in range(11):
            data = numpy.random.random((1024, 1024))
            writer.add_point(data)
            expected.append(data)
        writer.flush_buffer()
    with h5py.File(filename, mode="r") as f:
        data = f["data"][()]
    numpy.testing.assert_allclose(data, expected)
