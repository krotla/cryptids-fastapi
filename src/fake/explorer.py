from model.explorer import Explorer

from .common import check_duplicate, find

# fake data , replaced in the future by a real database and SQL
_explorers = [
    Explorer(
        name="Claude Hande",
        country="FR",
        description="Scarce during full moons",
    ),
    Explorer(
        name="Noah Weiser",
        country="DE",
        description="Myopic machete man",
    ),
]


def get_all() -> list[Explorer]:
    return _explorers


def get_one(name: str) -> Explorer:
    return find(_explorers, name)


def create(explorer: Explorer) -> Explorer:
    check_duplicate(_explorers, explorer.name)
    return explorer


def modify(name: str, explorer: Explorer) -> Explorer:
    find(_explorers, name)
    return explorer


def delete(name: str) -> None:
    find(_explorers, name)
