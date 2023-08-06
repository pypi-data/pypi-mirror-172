import os.path
import tempfile
import maptools


def test_mask(ideal_map_filename, mask_filename):

    for fourier_space in [True, False]:

        for shift in [True, False]:

            _, output_map_filename = tempfile.mkstemp()

            maptools.mask(
                ideal_map_filename,
                output_map_filename=output_map_filename,
                input_mask_filename=mask_filename,
                fourier_space=fourier_space,
                shift=shift,
            )

            assert os.path.exists(output_map_filename)
