import os

from fastapi import APIRouter, HTTPException, status

if os.getenv("CRYPTID_UNIT_TEST"):
    from fake import creature as service
else:
    from service import creature as service
from error import Duplicate, Missing
from model.creature import Creature

router = APIRouter(prefix="/creature")


@router.get("")
@router.get("/")
def get_all() -> list[Creature]:
    return service.get_all()


@router.get("/{name}")
def get_one(name) -> Creature | None:
    try:
        return service.get_one(name)
    except Missing as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ex.msg)


# all the remaining endpoints do nothing yet:
@router.post("", status_code=status.HTTP_201_CREATED)
@router.post("/", status_code=status.HTTP_201_CREATED)
def create(creature: Creature) -> Creature:
    try:
        return service.create(creature)
    except Duplicate as ex:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=ex.msg)


@router.patch("")
@router.patch("/")
def modify(name: str, creature: Creature) -> Creature:
    try:
        return service.modify(name, creature)
    except Missing as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ex.msg)


@router.delete("/{name}")
def delete(name: str):
    try:
        return service.delete(name)
    except Missing as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ex.msg)
