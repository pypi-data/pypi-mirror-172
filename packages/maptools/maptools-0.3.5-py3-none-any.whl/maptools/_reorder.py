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
from maptools.util import read, write, read_axis_order, write_axis_order


__all__ = ["reorder"]


# Get the logger
logger = logging.getLogger(__name__)


def reorder(*args, **kwargs):
    if len(args) == 0:
        return _reorder_str(**kwargs)
    return _reorder(*args, **kwargs)


@singledispatch
def _reorder(_):
    raise RuntimeError("Unexpected input")


@_reorder.register
def _reorder_str(
    input_map_filename, output_map_filename: str, axis_order: tuple = (0, 1, 2)
):
    """
    Reorder the data axes

    Args:
        input_map_filename: The input map filename
        output_map_filename: The output map filename
        axis_order: The axis order

    """

    # Open the input file
    infile = read(input_map_filename)

    # Get the axis order
    original_order = read_axis_order(infile)
    assert tuple(sorted(axis_order)) == (0, 1, 2)

    # Reorder the axes
    data = _reorder_ndarray(infile.data, original_order, axis_order)

    # Write the output file
    outfile = write(output_map_filename, data, infile=infile)
    write_axis_order(outfile, axis_order)
    outfile.update_header_stats()


@_reorder.register
def _reorder_ndarray(
    data: np.ndarray, original_order: tuple, new_order: tuple
) -> np.ndarray:
    """
    Reorder the data axes

    Args
        data: The data array
        original_order: The original order
        new_order: The new order

    Returns:
        The reordered data

    """

    def swap(x, a, b):
        x[a], x[b] = x[b], x[a]
        return x

    # Convert to list
    old_order = list(original_order)

    # Reorder the axes
    index = old_order.index(new_order[0])
    if index != 0:
        logger.info("Swapping axis %d with %d" % (0, index))
        data = np.swapaxes(data, 0, index)
        old_order = swap(old_order, 0, index)
    index = old_order.index(new_order[1])
    if index != 1:
        logger.info("Swapping axis %d with %d" % (1, index))
        data = np.swapaxes(data, 1, index)
        old_order = swap(old_order, 1, index)
    assert tuple(old_order) == tuple(new_order)

    # Return the reordered array
    return data
