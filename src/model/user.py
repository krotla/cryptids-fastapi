from pydantic import BaseModel


class User(BaseModel):
    name: str
    hash: str


class UserCreate(BaseModel):
    name: str
    password: str
