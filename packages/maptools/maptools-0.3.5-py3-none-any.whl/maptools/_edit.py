#
# Copyright (C) 2020 RFI
#
# Author: James Parkhurst
#
# This code is distributed under the GPLv3 license, a copy of
# which is included in the root directory of this package.
#
import logging
from maptools.util import read


__all__ = ["edit"]


# Get the logger
logger = logging.getLogger(__name__)


def edit(input_map_filename: str, voxel_size: tuple = None, origin: tuple = None):
    """
    Crop the map

    Args:
        input_filename: The input map filename
        voxel_size: The voxel size
        origin: The origin

    """

    # Open the input file
    infile = read(input_map_filename, mode="r+")

    # Set the voxel size
    if voxel_size is not None:
        if len(voxel_size) == 1:
            voxel_size = voxel_size[0]
        infile.voxel_size = voxel_size

    # Set the origin
    if origin is not None:
        infile.header.origin["z"] = origin[0]
        infile.header.origin["y"] = origin[1]
        infile.header.origin["x"] = origin[2]
