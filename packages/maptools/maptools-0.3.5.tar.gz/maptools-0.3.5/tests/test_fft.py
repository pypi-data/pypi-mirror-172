import os.path
import tempfile
import maptools


def test_fft(ideal_map_filename):

    for mode in ["real", "imaginary", "amplitude", "phase", "power"]:
        for shift in [True, False]:
            for normalize in [True, False]:

                _, output_map_filename = tempfile.mkstemp()

                maptools.fft(
                    input_map_filename=ideal_map_filename,
                    output_map_filename=output_map_filename,
                    mode=mode,
                    shift=shift,
                    normalize=normalize,
                )

                assert os.path.exists(output_map_filename)
