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
from typing import Tuple
from maptools.util import read, write


__all__ = ["rotate"]


# Get the logger
logger = logging.getLogger(__name__)


def rotate(
    input_map_filename: str,
    output_map_filename: str,
    axes: Tuple[int, int] = (0, 1),
    num: int = 1,
):
    """
    Rotate the map

    Args:
        input_map_filename: The input map filename
        output_map_filename: The output map filename
        axes: The axis to rotate around
        num: The number of times to rotate by 90 degrees

    """

    # Open the input file
    infile = read(input_map_filename)

    # Get data
    data = infile.data.copy()

    # Apply the threshold
    logger.info("Rotating %d times around axes %s" % (num, axes))
    data = np.rot90(data, k=num, axes=axes)

    # Write the output file
    write(output_map_filename, data, infile=infile)
