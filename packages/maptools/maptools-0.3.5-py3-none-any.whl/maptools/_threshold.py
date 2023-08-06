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
from functools import singledispatch
from maptools.util import read, write


__all__ = ["threshold"]


# Get the logger
logger = logging.getLogger(__name__)


def threshold(*args, **kwargs):
    if len(args) == 0:
        return _threshold_str(**kwargs)
    return _threshold(*args, **kwargs)


@singledispatch
def _threshold(_):
    raise RuntimeError("Unexpected input")


@_threshold.register
def _threshold_str(
    input_map_filename,
    output_map_filename: str,
    output_mask_filename: str = None,
    threshold: float = 0,
    normalize: bool = False,
    zero: bool = True,
):
    """
    Threshold the map

    Args:
        input_map_filename: The input map filename
        output_map_filename: The output map filename
        threshold: The threshold value
        normalize: Normalize the map before thresholding
        zero: Shift the data to zero

    """

    # Open the input file
    infile = read(input_map_filename)

    # Get data
    data = infile.data.copy()

    # Apply the threshold
    data, mask = _threshold_ndarray(
        data, threshold=threshold, normalize=normalize, zero=zero
    )

    # Write the output file
    write(output_map_filename, data, infile=infile)

    # Write the mask
    if output_mask_filename:
        write(output_mask_filename, mask.astype("uint8"), infile=infile)


@_threshold.register
def _threshold_ndarray(
    data: np.ndarray, threshold: float = 0, normalize: bool = False, zero: bool = True
) -> tuple:
    """
    Threshold the map

    Args:
        data: The input data
        threshold: The threshold value
        normalize: Normalize the map before thresholding
        zero: Shift the data to zero

    Returns:
        The thresholded array

    """

    # Apply the threshold
    logger.info("Apply threshold %f" % threshold)
    if normalize:
        data = (data - np.mean(data)) / np.std(data)
    mask = data >= threshold
    data[~mask] = threshold
    if zero:
        data -= threshold

    # Return the data
    return data, mask
