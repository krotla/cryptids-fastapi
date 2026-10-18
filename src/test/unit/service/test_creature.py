import os

os.environ["CRYPTID_UNIT_TEST"] = "true"
import pytest

from error import Duplicate, Missing
from model.creature import Creature
from service import creature as service


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
    return service.get_all()


def assert_duplicate(ex):
    assert "already exists!" in ex.value.msg


def assert_missing(ex):
    assert "not found!" in ex.value.msg


def test_create(sample):
    resp = service.create(sample)
    assert resp == sample


def test_creature_duplicate(fakes):
    with pytest.raises(Duplicate) as ex:
        service.create(fakes[0])
    assert_duplicate(ex)


def test_get_one_existed(fakes):
    resp = service.get_one(fakes[0].name)
    assert resp == fakes[0]


def test_get_one_missing():
    with pytest.raises(Missing) as ex:
        service.get_one("boxturtle")
    assert_missing(ex)


def test_modify(fakes):
    fakes[0].country = "CA"  # Canada!
    resp = service.modify(fakes[0].name, fakes[0])
    assert resp == fakes[0]


def test_modify_missing():
    bob: Creature = Creature(
        name="bob", country="US", area="*", description="some guy", aka="??"
    )
    with pytest.raises(Missing) as ex:
        _ = service.modify(bob.name, bob)
    assert_missing(ex)
