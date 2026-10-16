from typing import Protocol

from error import Duplicate, Missing


class HasName(Protocol):
    name: str


def find[T: HasName](fakes: list[T], name: str) -> T:
    for fake in fakes:
        if fake.name == name:
            return fake
    raise Missing(msg=f"Creature {name} not found!")


def check_duplicate[T: HasName](fakes: list[T], name: str):
    try:
        find(fakes, name)
        raise Duplicate(msg=f"Creature {name} already exists!")
    except Missing:
        pass
