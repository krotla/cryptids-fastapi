import os

from fastapi import APIRouter, HTTPException, status

if os.getenv("CRYPTID_UNIT_TEST"):
    from fake import explorer as service
else:
    from service import explorer as service
from error import Duplicate, Missing
from model.explorer import Explorer

router = APIRouter(prefix="/explorer")


@router.get("")
@router.get("/")
def get_all() -> list[Explorer]:
    return service.get_all()


@router.get("/{name}")
def get_one(name) -> Explorer | None:
    try:
        return service.get_one(name)
    except Missing as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ex.msg)


@router.post("", status_code=status.HTTP_201_CREATED)
@router.post("/", status_code=status.HTTP_201_CREATED)
def create(explorer: Explorer) -> Explorer:
    try:
        return service.create(explorer)
    except Duplicate as ex:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=ex.msg)


@router.patch("")
@router.patch("/")
def modify(name: str, explorer: Explorer) -> Explorer:
    try:
        return service.modify(name, explorer)
    except Missing as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ex.msg)


@router.delete("/{name}")
def delete(name: str):
    try:
        return service.delete(name)
    except Missing as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ex.msg)
