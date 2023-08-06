#
# Copyright (C) 2020 RFI
#
# Author: James Parkhurst
#
# This code is distributed under the GPLv3 license, a copy of
# which is included in the root directory of this package.
#
import gemmi
import logging
import numpy as np
import scipy.ndimage.morphology
from maptools.util import write


__all__ = ["genmask"]


# Get the logger
logger = logging.getLogger(__name__)


def genmask(
    input_pdb_filename: str,
    output_mask_filename: str,
    atom_radius: float = 5,
    border: int = 0,
    shape: tuple = (0, 0, 0),
    voxel_size: float = 1,
    sigma: float = 0,
):
    """
    Generate the mask

    Args:
        input_pdb_filename: The input pdb filename
        output_mask_filename: The output map filename
        atom_radius: The radius around the atoms
        border: The border of pixels
        shape: The shape of the output map
        voxel_size: The voxel size of the output map
        sigma: Soften the mask with a Gaussian edge

    """

    # Create the mask
    mask = np.ones(shape, dtype="bool")

    # Add a border
    mask[:border, :, :] = 0
    mask[-border - 1 :, :, :] = 0
    mask[:, :border, :] = 0
    mask[:, -border - 1 :, :] = 0
    mask[:, :, :border] = 0
    mask[:, :, -border - 1 :] = 0

    # Add atom mask
    if input_pdb_filename is not None:

        # Read the structure
        structure = gemmi.read_structure(input_pdb_filename)

        # Get the coordinates
        coords = np.array(
            [
                (atom.pos.z, atom.pos.y, atom.pos.x)
                for model in structure
                for chain in model
                for residue in chain
                for atom in residue
            ]
        ).T

        # Print some infor
        logger.info("Min / Max X: %f / %f" % (coords[2].min(), coords[2].max()))
        logger.info("Min / Max Y: %f / %f" % (coords[1].min(), coords[1].max()))
        logger.info("Min / Max Z: %f / %f" % (coords[0].min(), coords[0].max()))

        # Convert to indices
        index = np.floor(coords / voxel_size).astype("int32")
        atoms = np.ones(shape)
        atoms[index[0], index[1], index[2]] = 0

        # Compute distance and update mask
        distance = scipy.ndimage.morphology.distance_transform_edt(
            atoms, sampling=voxel_size
        )
        mask = mask & (distance <= atom_radius)

    # Soften the mask
    if sigma > 0:
        logger.info("Soften mask edge with sigma = %f" % sigma)
        distance = scipy.ndimage.morphology.distance_transform_edt(
            ~mask, sampling=voxel_size
        )
        mask = np.exp(-0.5 * distance**2 / sigma**2)

    # Write the output file
    outfile = write(output_mask_filename, mask.astype("float32"))
    outfile.voxel_size = voxel_size
