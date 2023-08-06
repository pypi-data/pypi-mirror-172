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
import maptools
from functools import singledispatch
from maptools.util import read, write, read_axis_order


__all__ = ["cc"]


# Get the logger
logger = logging.getLogger(__name__)


def cc(*args, **kwargs):
    if len(args) == 0:
        return _cc_str(**kwargs)
    return _cc(*args, **kwargs)


@singledispatch
def _cc(_):
    raise RuntimeError("Unexpected input")


@_cc.register
def _cc_str(
    input_map_filename1: str,
    input_map_filename2: str,
    output_map_filename: str,
):
    """
    Compute the CC between two maps

    Args:
        input_map_filename1: The input map filename
        input_map_filename2: The input map filename
        output_map_filename: The output cc filename

    """

    # Open the input file
    infile1 = read(input_map_filename1)

    # Get the data
    data1 = infile1.data
    if input_map_filename2 is not None:
        infile2 = read(input_map_filename2)
        data2 = infile2.data
        data2 = maptools.reorder(
            data2, read_axis_order(infile2), read_axis_order(infile1)
        )
    else:
        data2 = None

    # Compute the cc
    cc = _cc_ndarray(data1, data2)

    # Write the output file
    write(output_map_filename, cc.astype("float32"), infile=infile1)


@_cc.register
def _cc_ndarray(data1: np.ndarray, data2: np.ndarray = None) -> np.ndarray:
    """
    Compute the CC between two maps

    Args:
        data1: The input map 1
        data2: The input map 2

    Returns:
        array: The CC

    """

    # Compute the Fourier transform of the data
    fdata1 = np.fft.fftn((data1 - np.mean(data1)) / np.std(data1))

    # Transform data2
    if data2 is not None:
        fdata2 = np.fft.fftn((data2 - np.mean(data2)) / np.std(data2))
    else:
        fdata2 = fdata1

    # Compute the CC
    cc = np.fft.fftshift(np.real(np.fft.ifftn(fdata1 * np.conj(fdata2)))) / fdata1.size

    # Print some output
    logger.info("Min CC = %f, Max CC = %f" % (cc.min(), cc.max()))

    # Return the CC
    return cc
