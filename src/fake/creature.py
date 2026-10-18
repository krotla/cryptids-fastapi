from contextlib import nullcontext

from model.creature import Creature

from .common import check_duplicate, find

# fake data , replaced in the future by a real database and SQL
_creatures = [
    Creature(
        name="Yeti",
        aka="Abominable Snowman",
        country="CN",
        area="Himalayas",
        description="Hirsute Himalayan",
    ),
    Creature(
        name="Bigfoot",
        description="Yeti's Cousin Eddie",
        country="US",
        area="*",
        aka="Sasquatch",
    ),
]

transaction = nullcontext()


def get_all() -> list[Creature]:
    return _creatures


def get_one(name: str) -> Creature:
    return find(_creatures, name)


def create(creature: Creature) -> Creature:
    check_duplicate(_creatures, creature.name)
    return creature


def modify(name: str, creature: Creature) -> Creature:
    find(_creatures, name)
    return creature


def delete(name: str) -> None:
    find(_creatures, name)
