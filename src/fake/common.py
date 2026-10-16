from typing import Protocol

from error import Duplicate, Missing


class HasName(Protocol):
    name: str


def find[T: HasName](fakes: list[T], name: str) -> T:
    for fake in fakes:
        if fake.name == name:
            return fake
    raise Missing(msg=f"Missing user {name}")


def check_duplicate[T: HasName](fakes: list[T], name: str):
    if find(fakes, name):
        raise Duplicate(msg=f"Duplicate user {name}")
