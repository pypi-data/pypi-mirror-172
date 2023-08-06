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
import scipy.spatial.transform
from math import pi
from functools import singledispatch
from typing import Union
from maptools.util import read, write, read_axis_order


__all__ = ["transform"]


# Get the logger
logger = logging.getLogger(__name__)


def transform(*args, **kwargs):
    if len(args) == 0:
        return _transform_str(**kwargs)
    return _transform(*args, **kwargs)


@singledispatch
def _transform(_):
    raise RuntimeError("Unexpected input")


@_transform.register
def _transform_str(
    input_map_filename: str,
    output_map_filename: str,
    offset: tuple = None,
    rotation: tuple = (0, 0, 0),
    translation: tuple = (0, 0, 0),
    deg: bool = False,
):
    """
    Transform the map

    Args:
        input_map_filename: The input map filename
        output_map_filename: The output map filename
        offset: The offset to rotate about
        rotation: The rotation vector
        translation: The translation vector
        deg: Is the rotation in degrees

    """

    # Open the input file
    infile = read(input_map_filename)

    # Get the axis order
    axis_order = read_axis_order(infile)

    # Get data
    data = infile.data

    # Do the transform
    data = _transform_ndarray(
        data,
        axis_order=axis_order,
        offset=offset,
        rotation=rotation,
        translation=translation,
        deg=deg,
    )

    # Write the output file
    write(output_map_filename, data, infile=infile)


@_transform.register
def _transform_ndarray(
    data: np.ndarray,
    axis_order: tuple = (0, 1, 2),
    offset: Union[tuple, np.ndarray] = None,
    rotation: Union[tuple, np.ndarray] = (0, 0, 0),
    translation: Union[tuple, np.ndarray] = (0, 0, 0),
    deg: bool = False,
) -> np.ndarray:
    """
    Transform the map

    Args:
        data: The data to transform
        offset: The offset to rotate about
        rotation: The rotation vector
        translation: The translation vector
        deg: Is the rotation in degrees

    Returns:
        array: The transformed data

    """
    assert tuple(sorted(axis_order)) == (0, 1, 2)

    # Set the offset
    if offset is None:
        offset = np.array(data.shape) / 2
    else:
        offset = np.array(offset)
        offset = offset[axis_order]

    # Reorder input vectors
    translation = np.array(translation)[axis_order]
    rotation = np.array(rotation)[axis_order]

    # If the rotation is in degrees transform
    if deg:
        rotation = np.array(rotation) * pi / 180

    # Create the rotation matrix
    rotation = scipy.spatial.transform.Rotation.from_rotvec(rotation).as_matrix()
    O = np.diag((1.0, 1.0, 1.0, 1.0))
    T = np.diag((1.0, 1.0, 1.0, 1.0))
    T[0:3, 0:3] = rotation
    T[0:3, 3] = translation
    O[0:3, 3] = offset
    matrix = np.matmul(O, np.matmul(T, np.linalg.inv(O)))

    # Do the transformation
    logger.info("Performing transformation")
    logger.info("matrix=")
    logger.info(matrix)
    data = scipy.ndimage.affine_transform(data, np.linalg.inv(matrix))

    # Return the transformed data
    return data
