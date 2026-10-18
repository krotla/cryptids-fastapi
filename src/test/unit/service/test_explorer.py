import os

os.environ["CRYPTID_UNIT_TEST"] = "true"
import pytest

from error import Duplicate, Missing
from model.explorer import Explorer
from service import explorer as service


@pytest.fixture
def sample() -> Explorer:
    return Explorer(
        name="Robert Scott",
        country="GB",
        description="PEak south. Almost there!",
    )


@pytest.fixture
def fakes() -> list[Explorer]:
    return service.get_all()


def assert_duplicate(ex):
    assert "already exists!" in ex.value.msg


def assert_missing(ex):
    assert "not found!" in ex.value.msg


def test_create(sample):
    resp = service.create(sample)
    assert resp == sample


def test_explorer_duplicate(fakes):
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
    bob: Explorer = Explorer(name="Amundsen", country="DK", description="some guy")
    with pytest.raises(Missing) as ex:
        _ = service.modify(bob.name, bob)
    assert_missing(ex)
