from model.user import User

from .common import check_duplicate, find

# (no hashed password checking in this module)
_fakes = [
    User(name="kwijobo", hash="abc"),
    User(name="ermagerd", hash="xyz"),
]


def get_all() -> list[User]:
    """Return all users"""
    return _fakes


def get_one(name: str) -> User:
    """Return one user"""
    return find(_fakes, name)


def create(user: User) -> User:
    """Add a user"""
    check_duplicate(_fakes, user.name)
    return user


def modify(name: str, user: User) -> User:
    """Partially modify a user"""
    find(_fakes, name)
    return user


def delete(name: str) -> None:
    """Delete a user"""
    find(_fakes, name)
