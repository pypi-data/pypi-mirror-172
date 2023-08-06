#
# Copyright (C) 2020 RFI
#
# Author: James Parkhurst
#
# This code is distributed under the GPLv3 license, a copy of
# which is included in the root directory of this package.
#
import logging
import numpy as np
from maptools.util import read, write


__all__ = ["fft"]


# Get the logger
logger = logging.getLogger(__name__)


def fft(
    input_map_filename: str,
    output_map_filename: str,
    mode: str = "amplitude",
    shift: bool = True,
    normalize: bool = True,
):
    """
    Compute the FFT of the map

    Args:
        input_map_filename: The input map filename
        output_map_filename: The output map filename
        mode: The component to output
        shift: Shift the fourier components
        normalize: Normalize before computing FFT

    """

    # Open the input file
    infile = read(input_map_filename)

    # Get the subset of data
    logger.info("Computing FFT (%s)" % mode)

    # The data
    data = infile.data

    # Normalize if necessary
    if normalize:
        data = (data - np.mean(data)) / np.std(data)

    # Compute FFT
    data = {
        "real": lambda x: np.real(x),
        "imaginary": lambda x: np.imag(x),
        "amplitude": lambda x: np.abs(x),
        "phase": lambda x: np.angle(x),
        "power": lambda x: np.abs(x) ** 2,
    }[mode](np.fft.fftn(data).astype("complex64"))

    # Shift if necessary
    if shift:
        data = np.fft.fftshift(data)

    # Write the output file
    write(output_map_filename, data, infile=infile)
