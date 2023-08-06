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
import scipy.signal
from maptools.util import read, write
from functools import singledispatch


__all__ = ["rebin"]


# Get the logger
logger = logging.getLogger(__name__)


def rebin(*args, **kwargs):
    if len(args) == 0:
        return _rebin_str(**kwargs)
    return _rebin(*args, **kwargs)


@singledispatch
def _rebin(_):
    raise RuntimeError("Unexpected input")


@_rebin.register
def _rebin_str(input_map_filename: str, output_map_filename: str, shape: tuple):
    """
    Rebin the map

    Args:
        input_map_filename: The input map filename
        output_map_filename: The output map filename
        shape: The new shape of the map

    """

    # Open the input file
    infile = read(input_map_filename)

    # Get the data
    data = infile.data

    # Get the subset of data
    logger.info("Resampling map from shape %s to %s" % (data.shape, tuple(shape)))
    data = _rebin_ndarray(data, shape)

    # Write the output file
    outfile = write(output_map_filename, data, infile=infile)

    # Update the voxel size
    outfile.voxel_size = (
        outfile.voxel_size["z"] * infile.data.shape[0] // shape[0],
        outfile.voxel_size["y"] * infile.data.shape[1] // shape[1],
        outfile.voxel_size["x"] * infile.data.shape[2] // shape[2],
    )


# @_rebin.register
# def _rebin_ndarray(data, shape):
#    """
#    Rebin a multidimensional array
#
#    Args:
#        data (array): The input array
#        shape (tuple): The new shape
#
#    """
#
#    # Ensure dimensions are consistent
#    assert data.ndim == len(shape)
#    assert data.shape[0] % shape[0] == 0
#    assert data.shape[1] % shape[1] == 0
#    assert data.shape[2] % shape[2] == 0
#
#    # Get pairs of (shape, bin factor) for each dimension
#    factors = np.array([(d, c // d) for d, c in zip(shape, data.shape)])
#
#    # Rebin the array
#    data = data.reshape(factors.flatten())
#    for i in range(len(shape)):
#        data = data.sum(-1 * (i + 1))
#    return data


@_rebin.register
def _rebin_ndarray(data: np.ndarray, shape: tuple):
    """
    Rebin a multidimensional array

    Args:
        data: The input array
        shape: The new shape

    """
    # Get pairs of (shape, bin factor) for each dimension
    factors = np.array([(d, c // d) for d, c in zip(shape, data.shape)])

    # Rebin the array
    for i in range(len(factors)):
        data = scipy.signal.decimate(data, factors[i][1], axis=i)
    # data = data.reshape(factors.flatten())
    # for i in range(len(shape)):
    #     data = data.sum(-1 * (i + 1))
    return data
