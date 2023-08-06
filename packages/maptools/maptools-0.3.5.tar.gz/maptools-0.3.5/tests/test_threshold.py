import os.path
import tempfile
import maptools


def test_threshold(ideal_map_filename):

    for normalize in [True, False]:

        for zero in [True, False]:

            _, output_map_filename = tempfile.mkstemp()

            maptools.threshold(
                ideal_map_filename,
                output_map_filename=output_map_filename,
                threshold=0,
                normalize=normalize,
                zero=zero,
            )

            assert os.path.exists(output_map_filename)
