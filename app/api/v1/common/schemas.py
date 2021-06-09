from typing import Optional, List
from pydantic import BaseModel


# Project
class ProjectBase(BaseModel):
    name: Optional[str] = None


class ProjectCreate(ProjectBase):
    name: str


class ProjectInDBBase(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None

    class Config:
        orm_mode = True


class Project(ProjectInDBBase):
    name: str


class ProjectWithStudies(ProjectInDBBase):
    subjects: List[str]


# Subject
class SubjectBase(BaseModel):
    name: Optional[str] = None


class SubjectCreate(SubjectBase):
    name: str


class SubjectInDBBase(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None

    class Config:
        orm_mode = True


class Subject(SubjectInDBBase):
    name: str


class SubjectWithStudies(SubjectInDBBase):
    studies: List[str]
