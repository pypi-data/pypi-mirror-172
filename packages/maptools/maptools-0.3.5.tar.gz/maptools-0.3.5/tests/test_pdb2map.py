import os.path
import tempfile
import maptools
import maptools.external
import pytest


@pytest.mark.skipif(not maptools.external.is_ccp4_available(), reason="requires CCP4")
def test_pdb2map(pdb_filename):

    _, output_filename = tempfile.mkstemp()

    maptools.pdb2map(
        pdb_filename,
        output_map_filename=output_filename,
        resolution=8,
        grid=(200, 200, 200),
    )

    assert os.path.exists(output_filename)
