import os

import pytest

from error import Duplicate, Missing
from model.user import User

# set this before data imports below for data.init
os.environ["CRYPTID_SQLITE_DB"] = ":memory:"
from data import user


@pytest.fixture
def sample() -> User:
    return User(name="Martin", hash="hashedpassword")


def test_create(sample):
    resp = user.create(sample)
    assert resp == sample


def test_create_duplicate(sample):
    with pytest.raises(Duplicate):
        _ = user.create(sample)


def test_get_one(sample):
    resp = user.get_one(sample.name)
    assert resp == sample


def test_get_one_missing(sample):
    with pytest.raises(Missing):
        _ = user.get_one("John")


def test_modify(sample):
    sample.hash = "newerhashedpassword"
    resp = user.modify(sample.name, sample)
    assert resp == sample


def test_modify_missing(sample):
    person: User = User(name="John", hash="johnshash")
    with pytest.raises(Missing):
        _ = user.modify(person.name, person)


def test_delete(sample):
    resp = user.delete(sample.name)
    assert resp is None


def test_delete_missing(sample):
    with pytest.raises(Missing):
        _ = user.delete(sample.name)
