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
import scipy.ndimage.measurements
import skimage.filters
import maptools
from functools import singledispatch
from maptools.util import read, write


__all__ = ["segment"]


# Get the logger
logger = logging.getLogger(__name__)


def segment(*args, **kwargs):
    if len(args) == 0:
        return _segment_str(**kwargs)
    return _segment(*args, **kwargs)


@singledispatch
def _segment(_):
    raise RuntimeError("Unexpected input")


@_segment.register
def _segment_str(
    input_map_filename: str,
    output_map_filename: str = None,
    output_mask_filename: str = None,
    num_objects: int = 1,
):
    """
    Segment the map

    Args:
        input_map_filename: The input map filename
        output_map_filename: The output map filename
        output_mask_filename: The output mask filename
        num_objects: The number of objects

    """

    # Open the input file
    infile = read(input_map_filename)

    # Get data
    data = infile.data

    # Segment the data
    mask = _segment_ndarray(data, num_objects=num_objects)

    # Write the output file
    if output_mask_filename is not None:
        write(output_mask_filename, mask, infile=infile)
    if output_map_filename is not None:
        write(output_map_filename, maptools.mask(data, mask), infile=infile)


@_segment.register
def _segment_ndarray(data: np.ndarray, num_objects: int = 1):
    """
    Segment the map

    Args:
        data: The input data
        num_objects: The number of objects

    Returns:
        array: The segmented array

    """

    # Compute a threshold value
    threshold = skimage.filters.threshold_otsu(data)
    logger.info("Using threshold = %f" % threshold)

    # Label the pixels
    labels, num_labels = scipy.ndimage.label((data >= threshold).astype("int8"))
    logger.info("Found %d objects" % num_labels)

    # Compute the largest objects
    num_pixels = np.bincount(labels.flatten())
    sorted_indices = np.argsort(num_pixels[1:])[::-1] + 1
    result = np.zeros(shape=data.shape, dtype="uint8")
    for index in sorted_indices[:num_objects]:
        logger.info("Selecting object with %d pixels" % num_pixels[index])
        result[labels == index] = 1

    # Return the data
    return result
