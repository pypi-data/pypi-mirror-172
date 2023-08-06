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
import scipy.ndimage
import maptools
from functools import singledispatch
from maptools.util import read, write, read_axis_order


__all__ = ["fsc3d"]


# Get the logger
logger = logging.getLogger(__name__)


def fsc3d(*args, **kwargs):
    if len(args) == 0:
        return _fsc3d_str(**kwargs)
    return _fsc3d(*args, **kwargs)


@singledispatch
def _fsc3d(_):
    raise RuntimeError("Unexpected input")


@_fsc3d.register
def _fsc3d_str(
    input_map_filename1: str,
    input_map_filename2: str,
    output_map_filename: str,
    kernel: int = 9,
    resolution: float = None,
):
    """
    Compute the local FSC of the map

    Args:
        input_map_filename1 (str): The input map filename
        input_map_filename2 (str): The input map filename
        output_map_filename (str): The output map filename
        kernel (int): The kernel size
        resolution (float): The resolution limit

    """

    # Open the input files
    infile1 = read(input_map_filename1)
    infile2 = read(input_map_filename2)

    # Get the data
    data1 = infile1.data
    data2 = infile2.data

    # Reorder input arrays
    data1 = maptools.reorder(data1, read_axis_order(infile1), (0, 1, 2))
    data2 = maptools.reorder(data2, read_axis_order(infile2), (0, 1, 2))

    # Get voxel size
    voxel_size = (
        infile1.voxel_size["z"],
        infile1.voxel_size["y"],
        infile1.voxel_size["x"],
    )

    # Compute the local FSC
    fsc = _fsc3d_ndarray(
        data1,
        data2,
        kernel=kernel,
        resolution=resolution,
        voxel_size=voxel_size,
    )

    # Reorder output array
    fsc = maptools.reorder(fsc, (0, 1, 2), read_axis_order(infile1))

    # Write the output file
    write(output_map_filename, fsc.astype("float32"), infile=infile1)


@_fsc3d.register
def _fsc3d_ndarray(
    data1: np.ndarray,
    data2: np.ndarray,
    kernel: int = 9,
    resolution: float = None,
    voxel_size: tuple = (1, 1, 1),
) -> np.ndarray:
    """
    Compute the local FSC of the map

    Args:
        data1: The input map 1
        data2: The input map 2
        kernel: The kernel size
        resolution: The resolution limit

    Returns:
        The local FSC map

    """

    # Get the subset of data
    logger.info("Computing local FSC")

    # Normalize the data
    data1 = (data1 - np.mean(data1)) / np.std(data1)
    data2 = (data2 - np.mean(data2)) / np.std(data2)

    # Compute the FFT of the data
    X = np.fft.fftshift(np.fft.fftn(data1))
    Y = np.fft.fftshift(np.fft.fftn(data2))

    # Compute local variance and covariance
    varX = scipy.ndimage.uniform_filter(np.abs(X) ** 2, size=kernel, mode="nearest")
    varY = scipy.ndimage.uniform_filter(np.abs(Y) ** 2, size=kernel, mode="nearest")
    covXY = scipy.ndimage.uniform_filter(
        np.real(X * np.conj(Y)), size=kernel, mode="nearest"
    )

    # Compute the FSC
    fsc = np.zeros(covXY.shape)
    tiny = 1e-5
    mask = (varX > tiny) & (varY > tiny)
    fsc[mask] = covXY[mask] / (np.sqrt(varX[mask]) * np.sqrt(varY[mask]))

    # Create a resolution mask
    if resolution is not None:
        shape = fsc.shape
        Z, Y, X = np.mgrid[0 : shape[0], 0 : shape[1], 0 : shape[2]]
        Z = (1.0 / voxel_size[0]) * (Z - shape[0] // 2) / shape[0]
        Y = (1.0 / voxel_size[1]) * (Y - shape[1] // 2) / shape[1]
        X = (1.0 / voxel_size[2]) * (X - shape[2] // 2) / shape[2]
        R = np.sqrt(X**2 + Y**2 + Z**2)
        mask = R < 1.0 / resolution
        fsc *= mask

    # Print some output
    logger.info("Min CC = %f, Max CC = %f" % (fsc.min(), fsc.max()))

    # Return the fsc
    return fsc
