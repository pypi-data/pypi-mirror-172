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
import scipy.ndimage.morphology
from functools import singledispatch
from maptools.util import read, write


__all__ = ["dilate"]


# Get the logger
logger = logging.getLogger(__name__)


def dilate(*args, **kwargs):
    if len(args) == 0:
        return _dilate_str(**kwargs)
    return _dilate(*args, **kwargs)


@singledispatch
def _dilate(_):
    raise RuntimeError("Unexpected input")


@_dilate.register
def _dilate_str(
    input_map_filename: str,
    output_map_filename: str,
    kernel: int = 3,
    num_iter: int = 1,
):
    """
    Dilate the map

    Args:
        input_map_filename: The input map filename
        output_map_filename: The output map filename
        kernel: The kernel size
        num_iter: The number of iterations

    """

    # Open the input file
    infile = read(input_map_filename)

    # Get the subset of data
    logger.info("Dilating map")
    data = _dilate_ndarray(infile.data, kernel=kernel, num_iter=num_iter)

    # Write the output file
    write(output_map_filename, data.astype("uint8"), infile=infile)


@_dilate.register
def _dilate_ndarray(data: np.ndarray, kernel: int = 3, num_iter: int = 1) -> np.ndarray:
    """
    Dilate the map

    Args:
        data: The array
        kernel: The kernel size
        num_iter: The number of iterations

    """
    # Generate a mask
    z, y, x = np.mgrid[0:kernel, 0:kernel, 0:kernel]
    z = z - kernel // 2
    y = y - kernel // 2
    x = x - kernel // 2
    r = np.sqrt(x**2 + y**2 + z**2)
    mask = r <= kernel // 2

    # Do the dilation
    return scipy.ndimage.morphology.binary_dilation(data, mask, num_iter)
