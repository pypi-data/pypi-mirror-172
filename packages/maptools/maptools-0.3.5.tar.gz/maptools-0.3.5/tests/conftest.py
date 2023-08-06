import os.path
import pytest


@pytest.fixture
def ideal_map_filename():
    return os.path.join(os.path.dirname(__file__), "ideal.mrc")


@pytest.fixture
def rec_map_filename():
    return os.path.join(os.path.dirname(__file__), "rec.mrc")


@pytest.fixture
def mask_filename():
    return os.path.join(os.path.dirname(__file__), "mask.mrc")


@pytest.fixture
def pdb_filename():
    return os.path.join(os.path.dirname(__file__), "4v1w.pdb")
