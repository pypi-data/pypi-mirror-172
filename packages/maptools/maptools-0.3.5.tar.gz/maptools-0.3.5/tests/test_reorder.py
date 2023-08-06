import os.path
import tempfile
import maptools


def test_reorder(ideal_map_filename):

    _, output_map_filename = tempfile.mkstemp()

    maptools.reorder(
        ideal_map_filename,
        output_map_filename=output_map_filename,
        axis_order=(0, 1, 2),
    )

    assert os.path.exists(output_map_filename)
