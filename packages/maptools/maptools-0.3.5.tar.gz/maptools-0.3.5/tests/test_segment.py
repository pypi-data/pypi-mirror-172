import os.path
import tempfile
import maptools


def test_threshold(ideal_map_filename):

    for normalize in [True, False]:

        for zero in [True, False]:

            _, output_map_filename = tempfile.mkstemp()
            _, output_mask_filename = tempfile.mkstemp()

            maptools.segment(
                ideal_map_filename,
                output_map_filename=output_map_filename,
                output_mask_filename=output_mask_filename,
            )

            assert os.path.exists(output_map_filename)
            assert os.path.exists(output_mask_filename)
