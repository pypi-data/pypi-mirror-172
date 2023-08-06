import os.path
import tempfile
import maptools


def test_transform(ideal_map_filename):

    _, output_map_filename = tempfile.mkstemp()

    maptools.transform(
        ideal_map_filename,
        output_map_filename=output_map_filename,
        offset=None,
        rotation=(0, 45, 0),
        translation=(10, 10, 10),
        deg=True,
    )

    assert os.path.exists(output_map_filename)
