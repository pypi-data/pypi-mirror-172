import os.path
import tempfile
import maptools


def test_rebin(ideal_map_filename):

    _, output_map_filename = tempfile.mkstemp()

    maptools.rebin(
        ideal_map_filename,
        output_map_filename=output_map_filename,
        shape=(25, 25, 25),
    )

    assert os.path.exists(output_map_filename)
