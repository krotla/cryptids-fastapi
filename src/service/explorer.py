import data.explorer as data
from model.explorer import Explorer


def get_all() -> list[Explorer]:
    return data.get_all()


def get_one(name: str) -> Explorer | None:
    return data.get_one(name)


def create(explorer: Explorer) -> Explorer:
    with data.transaction:
        return data.create(explorer)


def replace(explorer: Explorer) -> Explorer:
    return data.replace(explorer)


def modify(name: str, explorer: Explorer) -> Explorer:
    with data.transaction:
        return data.modify(name, explorer)


def delete(name: str) -> bool:
    with data.transaction:
        return data.delete(name)
