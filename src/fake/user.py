from error import Duplicate, Missing
from model.user import User

# (no hashed password checking in this module)
fakes = [
    User(name="kwijobo", hash="abc"),
    User(name="ermagerd", hash="xyz"),
]


def find(name: str) -> User:
    for fake in fakes:
        if fake.name == name:
            return fake
    raise Missing(msg=f"Missing user {name}")


def check_duplicate(name: str):
    if find(name):
        raise Duplicate(msg=f"Duplicate user {name}")


def get_all() -> list[User]:
    """Return all users"""
    return fakes


def get_one(name: str) -> User:
    """Return one user"""
    return find(name)


def create(user: User) -> User:
    """Add a user"""
    check_duplicate(user.name)
    return user


def modify(name: str, user: User) -> User:
    """Partially modify a user"""
    find(name)
    return user


def delete(name: str) -> None:
    """Delete a user"""
    find(name)
