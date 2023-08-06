import os.path
import tempfile
import maptools


def test_rotate(ideal_map_filename):

    for axes in [(0, 1), (0, 2), (1, 2)]:

        _, output_map_filename = tempfile.mkstemp()

        maptools.rotate(
            ideal_map_filename,
            output_map_filename=output_map_filename,
            axes=axes,
        )

        assert os.path.exists(output_map_filename)
