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


__all__ = ["rescale"]


# Get the logger
logger = logging.getLogger(__name__)


def rescale(*args, **kwargs):
    if len(args) == 0:
        return _rescale_str(**kwargs)
    return _rescale(*args, **kwargs)


@singledispatch
def _rescale(_):
    raise RuntimeError("Unexpected input")


@_rescale.register
def _rescale_str(
    input_map_filename: str,
    output_map_filename: str,
    mean: float = None,
    sdev: float = None,
    vmin: float = None,
    vmax: float = None,
    scale: float = None,
    offset: float = None,
):
    """
    Rescale the map

    Args:
        input_map_filename: The input map filename
        output_map_filename: The output map filename
        mean: The desired mean value
        sdev: The desired sdev value
        vmin: The desired min value
        vmax: The desired max value
        scale: The scale
        offset: The offset

    """

    # Open the input file
    infile = read(input_map_filename)

    # Get the data
    data = infile.data

    # Rescale the map
    data = _rescale_ndarray(
        data, mean=mean, sdev=sdev, vmin=vmin, vmax=vmax, scale=scale, offset=offset
    )

    # Write the output file
    write(output_map_filename, data, infile=infile)


@_rescale.register
def _rescale_ndarray(
    data: np.ndarray,
    mean: float = None,
    sdev: float = None,
    vmin: float = None,
    vmax: float = None,
    scale: float = None,
    offset: float = None,
) -> np.ndarray:
    """
    Rescale the map

    Args:
        data: The input map
        mean: The desired mean value
        sdev: The desired sdev value
        vmin: The desired min value
        vmax: The desired max value
        scale: The scale
        offset: The offset

    Returns:
        The output map

    """

    # Normalize by mean and standard deviation
    if mean is not None or sdev is not None:
        original_mean = np.mean(data)
        original_sdev = np.std(data)
        if mean is None:
            mean = original_mean
        if sdev is None:
            sdev = original_sdev
        scale = sdev / original_sdev
        offset = mean - original_mean * scale

    # Normalize by min and max
    if vmin is not None or vmax is not None:
        original_min = np.min(data)
        original_max = np.max(data)
        if vmin is None:
            vmin = original_mean
        if vmax is None:
            vmax = original_sdev
        scale = (vmax - vmin) / (original_max - original_min)
        offset = vmin - original_min * scale

    # If the scale and offset are set
    if scale is None:
        scale = 1
    if offset is None:
        offset = 0

    # Get the subset of data
    logger.info("Rescaling map with scale = %g and offset = %g" % (scale, offset))
    data = data * scale + offset
    logger.info(
        "Data min = %g, max = %g, mean = %g, sdev = %g"
        % (data.min(), data.max(), np.mean(data), np.std(data))
    )

    # Return the rescaled map
    return data
