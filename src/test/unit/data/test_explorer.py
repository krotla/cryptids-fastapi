import os

import pytest

from error import Duplicate, Missing
from model.explorer import Explorer

# set this before data imports below for data.init
os.environ["CRYPTID_SQLITE_DB"] = ":memory:"
from data import explorer


@pytest.fixture
def sample() -> Explorer:
    return Explorer(
        name="Indiana Jones",
        country="US",
        description="Snake hater",
    )


def test_create(sample):
    resp = explorer.create(sample)
    assert resp == sample


def test_create_duplicate(sample):
    with pytest.raises(Duplicate):
        _ = explorer.create(sample)


def test_get_one(sample):
    resp = explorer.get_one(sample.name)
    assert resp == sample


def test_get_one_missing(sample):
    with pytest.raises(Missing):
        _ = explorer.get_one("Lara Croft")


def test_modify(sample):
    sample.country = "PL"
    resp = explorer.modify(sample.name, sample)
    assert resp == sample


def test_modify_missing(sample):
    thing: Explorer = Explorer(
        name="Lara Croft", country="US", description="Tomb Rider"
    )
    with pytest.raises(Missing):
        _ = explorer.modify(thing.name, thing)


def test_delete(sample):
    resp = explorer.delete(sample.name)
    assert resp is None


def test_delete_missing(sample):
    with pytest.raises(Missing):
        _ = explorer.delete(sample.name)
