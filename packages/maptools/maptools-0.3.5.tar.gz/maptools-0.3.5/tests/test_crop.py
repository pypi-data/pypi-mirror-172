import os.path
import tempfile
import maptools


def test_crop(ideal_map_filename):

    _, output_map_filename = tempfile.mkstemp()

    maptools.crop(
        input_map_filename=ideal_map_filename,
        output_map_filename=output_map_filename,
        roi=(50, 60, 70, 100, 90, 80),
    )

    assert os.path.exists(output_map_filename)
