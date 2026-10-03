from fastapi import APIRouter, HTTPException, status

import service.explorer as service
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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ex.msg)


@router.patch("")
@router.patch("/")
def modify(name: str, explorer: Explorer) -> Explorer:
    try:
        return service.modify(name, explorer)
    except Missing as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ex.msg)


@router.put("")
@router.put("/")
def replace(explorer: Explorer) -> Explorer:
    return service.replace(explorer)


@router.delete("/{name}")
def delete(name: str) -> bool:
    try:
        return service.delete(name)
    except Missing as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ex.msg)
