from typing import Protocol

from error import Duplicate, Missing


class HasName(Protocol):
    name: str


def find[T: HasName](fakes: list[T], name: str) -> T:
    for fake in fakes:
        if fake.name == name:
            return fake
    class_name = type(fakes[0]).__name__ if fakes else "Item"
    raise Missing(msg=f"{class_name} {name} not found!")


def check_duplicate[T: HasName](fakes: list[T], name: str):
    try:
        find(fakes, name)
        class_name = type(fakes[0]).__name__ if fakes else "Item"
        raise Duplicate(msg=f"{class_name} {name} already exists!")
    except Missing:
        pass
