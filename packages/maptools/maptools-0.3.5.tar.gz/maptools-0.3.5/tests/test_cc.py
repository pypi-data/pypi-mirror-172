import os.path
import tempfile
import maptools


def test_cc(ideal_map_filename, rec_map_filename):

    # Test cross correlation
    _, output_map_filename = tempfile.mkstemp()

    maptools.cc(
        input_map_filename1=ideal_map_filename,
        input_map_filename2=rec_map_filename,
        output_map_filename=output_map_filename,
    )

    assert os.path.exists(output_map_filename)

    # Test auto correlation
    _, output_map_filename = tempfile.mkstemp()

    maptools.cc(
        input_map_filename1=ideal_map_filename,
        input_map_filename2=None,
        output_map_filename=output_map_filename,
    )

    assert os.path.exists(output_map_filename)
