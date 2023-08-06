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


__all__ = ["mask"]


# Get the logger
logger = logging.getLogger(__name__)


def mask(*args, **kwargs):
    if len(args) == 0:
        return _mask_str(**kwargs)
    return _mask(*args, **kwargs)


@singledispatch
def _mask(_):
    raise RuntimeError("Unexpected input")


@_mask.register
def _mask_str(
    input_map_filename,
    output_map_filename: str,
    input_mask_filename: str,
    fourier_space: bool = False,
    shift: bool = False,
):
    """
    Mask the map

    Args:
        input_map_filename: The input map filename
        output_map_filename: The output map filename
        input_mask_filename: The mask filename
        fourier_space: Apply in real space or fourier space
        shift: Shift the mask

    """

    # Open the input file
    infile = read(input_map_filename)

    # Open the mask file
    maskfile = read(input_mask_filename)

    # Apply the mask
    data = infile.data
    mask = maskfile.data

    # Reorder the maskfile axes to match the data
    mask = maptools.reorder(mask, read_axis_order(maskfile), read_axis_order(infile))

    # Apply the mask
    data = _mask_ndarray(data, mask, fourier_space=fourier_space, shift=shift)

    # Write the output file
    write(output_map_filename, data.astype("float32"), infile=infile)


@_mask.register
def _mask_ndarray(
    data: np.ndarray,
    mask: np.ndarray,
    value: int = 0,
    zero: bool = True,
    fourier_space: bool = False,
    shift: bool = False,
) -> np.ndarray:
    """
    Mask the map

    Args:
        data (array): The map
        mask (array): The mask
        space (str): Apply in real space or fourier space
        shift (bool): Shift the mask

    Returns:
        array: The masked map

    """

    # Apply mask
    if shift:
        logger.info("Shifting mask")
        mask = np.fft.fftshift(mask)
    if not fourier_space:
        logger.info("Applying mask in real space")
        data = data * mask
        # mask = mask > 0
        # data = data * mask + (~mask) * value
        # if zero:
        #     masked_data = data[mask]
        #     data[mask] = masked_data - np.min(masked_data) + value
    else:
        logger.info("Applying mask in Fourier space")
        data = np.real(np.fft.ifftn(np.fft.fftn(data) * mask))

    # Return the masked map
    return data
