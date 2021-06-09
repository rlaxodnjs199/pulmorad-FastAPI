from typing import Optional, List, Dict
from pydantic import BaseModel


class Study(BaseModel):
    id: int
    instance_uid: str
    project_title: str
    access_number: Optional[str]
    patient_id: str
    patient_name: str
    study_date: Optional[str]
    study_description: Optional[str]
    modalities: Optional[str]

    class Config:
        orm_mode = True


class Project(BaseModel):
    id: int
    title: str
    studies: List[Study] = []

    class Config:
        orm_mode = True


class ProjectCreate(BaseModel):
    title: str
