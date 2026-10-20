import os

import plotly.express as px
from fastapi import APIRouter, HTTPException, Response, status

if os.getenv("CRYPTID_UNIT_TEST"):
    from fake import creature as service
else:
    from service import creature as service
from collections import Counter

import country_converter as coco

from error import Duplicate, Missing
from model.creature import Creature

router = APIRouter(prefix="/creature")


@router.get("")
@router.get("/")
def get_all() -> list[Creature]:
    return service.get_all()


@router.get("/test")
def test():
    df = px.data.iris()
    fig = px.scatter(df, x="sepal_width", y="sepal_length", color="species")
    fig_bytes = fig.to_image(format="png")
    return Response(content=fig_bytes, media_type="image/png")


@router.get("/plot")
def plot():
    creatures = service.get_all()
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    counts = Counter(creature.name[0] for creature in creatures)
    y = {letter: counts.get(letter, 0) for letter in letters}
    fig = px.histogram(
        x=list(letters),
        y=y,
        title="Creature Names",
        labels={"x": "Initial", "y": "Initial"},
    )
    fig_bytes = fig.to_image(format="png")
    return Response(content=fig_bytes, media_type="image/png")


@router.get("/map")
def map():
    creatures = service.get_all()
    iso2_codes = (creature.country for creature in creatures)
    iso3_codes = coco.convert(names=iso2_codes, to="ISO3")
    fig = px.choropleth(locationmode="ISO-3", locations=iso3_codes)
    fig_bytes = fig.to_image(format="png")
    return Response(content=fig_bytes, media_type="image/png")


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
