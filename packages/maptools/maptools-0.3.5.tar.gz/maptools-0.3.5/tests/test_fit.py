import os.path
import tempfile
import maptools
import maptools.external
import pytest


@pytest.mark.skipif(not maptools.external.is_ccp4_available(), reason="requires CCP4")
def test_fit(ideal_map_filename, pdb_filename):

    _, output_pdb_filename = tempfile.mkstemp()
    _, log_filename = tempfile.mkstemp()

    maptools.fit(
        input_map_filename=ideal_map_filename,
        input_pdb_filename=pdb_filename,
        output_pdb_filename=output_pdb_filename,
        mode="rigid_body",
        resolution=8,
        ncycle=2,
        log_filename=log_filename,
    )

    assert os.path.exists(output_pdb_filename)
