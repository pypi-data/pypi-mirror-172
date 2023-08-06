import os.path
import tempfile
import maptools
import maptools.external
import pytest


@pytest.mark.skipif(not maptools.external.is_ccp4_available(), reason="requires CCP4")
def test_map2mtz(ideal_map_filename):

    _, output_filename = tempfile.mkstemp()

    maptools.map2mtz(
        ideal_map_filename,
        output_hkl_filename=output_filename,
        resolution=8,
    )

    assert os.path.exists(output_filename)
