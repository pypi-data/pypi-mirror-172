import os.path
import tempfile
import maptools


def test_fsc3d(ideal_map_filename, rec_map_filename):

    for axes in [0, 1, 2, (0, 1), (0, 2), (1, 2), (0, 1, 2), None]:

        _, output_map_filename = tempfile.mkstemp()

        maptools.fsc3d(
            input_map_filename1=ideal_map_filename,
            input_map_filename2=rec_map_filename,
            output_map_filename=output_map_filename,
            kernel=9,
            resolution=3,
        )

        assert os.path.exists(output_map_filename)
