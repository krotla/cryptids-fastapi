import os

import pytest
from fastapi import HTTPException

os.environ["CRYPTID_UNIT_TEST"] = "true"
from model.creature import Creature
from web import creature


@pytest.fixture
def sample() -> Creature:
    return Creature(
        name="dragon",
        country="*",
        area="Mountains",
        description="Wings! Fire! Aieee!",
        aka="The Ashmaker",
    )


@pytest.fixture
def fakes() -> list[Creature]:
    return creature.get_all()


def assert_duplicate(ex):
    assert ex.value.status_code == 409
    assert "already exists!" in ex.value.detail


def assert_missing(ex):
    assert ex.value.status_code == 404
    assert "not found!" in ex.value.detail


def test_create(sample):
    assert creature.create(sample) == sample


def test_create_duplicate(fakes):
    with pytest.raises(HTTPException) as ex:
        _ = creature.create(fakes[0])

    assert_duplicate(ex)


def test_get_one(fakes):
    assert creature.get_one(fakes[0].name) == fakes[0]


def test_get_one_missing():
    with pytest.raises(HTTPException) as ex:
        _ = creature.get_one("bobcat")

    assert_missing(ex)


def test_modify(fakes):
    assert creature.modify(fakes[0].name, fakes[0]) == fakes[0]


def test_modify_missing(sample):
    with pytest.raises(HTTPException) as ex:
        _ = creature.modify(sample.name, sample)

    assert_missing(ex)


def test_delete(fakes):
    assert creature.delete(fakes[0].name) is None


def test_delete_missing(sample):
    with pytest.raises(HTTPException) as ex:
        _ = creature.delete("emu")

    assert_missing(ex)
