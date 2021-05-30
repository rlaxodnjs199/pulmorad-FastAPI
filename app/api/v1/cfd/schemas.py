from app.db.pgsql.base_model import Base
from typing import List
from pydantic import BaseModel


class Image(BaseModel):
    id: int
    url: str

    class Config:
        orm_mode = True


class Subject(BaseModel):
    id: int
    name: str
    images: List[Image] = []

    class Config:
        orm_mode = True


class SubjectCreate(BaseModel):
    name: str


class CreateImage(BaseModel):
    url: str
