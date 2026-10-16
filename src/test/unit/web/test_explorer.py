import os

import pytest
from fastapi import HTTPException

os.environ["CRYPTID_UNIT_TEST"] = "true"
from model.explorer import Explorer
from web import explorer


@pytest.fixture
def sample() -> Explorer:
    return Explorer(
        name="Robert Scott",
        country="GB",
        description="PEak south. Almost there!",
    )


@pytest.fixture
def fakes() -> list[Explorer]:
    return explorer.get_all()


def assert_duplicate(ex):
    assert ex.value.status_code == 409
    assert "already exists!" in ex.value.detail


def assert_missing(ex):
    assert ex.value.status_code == 404
    assert "not found!" in ex.value.detail


def test_create(sample):
    assert explorer.create(sample) == sample


def test_create_duplicate(fakes):
    with pytest.raises(HTTPException) as ex:
        _ = explorer.create(fakes[0])

    assert_duplicate(ex)


def test_get_one(fakes):
    assert explorer.get_one(fakes[0].name) == fakes[0]


def test_get_one_missing():
    with pytest.raises(HTTPException) as ex:
        _ = explorer.get_one("Roald Amundsen")

    assert_missing(ex)


def test_modify(fakes):
    assert explorer.modify(fakes[0].name, fakes[0]) == fakes[0]


def test_modify_missing(sample):
    with pytest.raises(HTTPException) as ex:
        _ = explorer.modify(sample.name, sample)

    assert_missing(ex)


def test_delete(fakes):
    assert explorer.delete(fakes[0].name) is None


def test_delete_missing(sample):
    with pytest.raises(HTTPException) as ex:
        _ = explorer.delete("Roald Amundsen")

    assert_missing(ex)
