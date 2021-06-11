from typing import List
from fastapi import APIRouter
from fastapi.param_functions import Depends

from app.db.pgsql.session import get_db
from . import schemas, util

project_router = project = APIRouter(prefix='/projects')
subject_router = subject = APIRouter(prefix='/subjects')
study_router = study = APIRouter(prefix='/studies')


@project.get('/{project_id}', response_model=schemas.Project)
async def get_project(project_id: int, db=Depends(get_db)):
    return util.get_project(project_id, db)


@project.get('/', response_model=List[schemas.Project])
async def get_projects(db=Depends(get_db)):
    return util.get_projects(db)


@project.post('/', response_model=schemas.Project)
async def add_project(project: schemas.ProjectCreate, db=Depends(get_db)):
    return util.add_project(project, db)


@project.put('/{project_id}', response_model=schemas.Project)
async def update_project(project_id: int, new_name: str, db=Depends(get_db)):
    return util.update_project(project_id, new_name, db)


@project.delete('/{project_id}', response_model=schemas.Project)
async def delete_project(project_id: int, db=Depends(get_db)):
    return util.delete_project(project_id, db)


@project.get('/{project_id}/subjects', response_model=List[schemas.Subject])
async def get_subjects_from_project(project_id: int, db=Depends(get_db)):
    return util.get_subjects_from_project(project_id, db)


@project.post('/{project_id}/subjects/{subject_id}')
async def assign_subject_to_project(project_id: int, subject_id: int, db=Depends(get_db)):
    return util.assign_subject_to_project(project_id, subject_id, db)


@project.delete('/{project_id}/subjects/{subject_id}')
async def unassign_subject_from_project(project_id: int, subject_id: int, db=Depends(get_db)):
    return util.unassign_subject_from_project(project_id, subject_id, db)


@subject.get('/{subject_id}', response_model=schemas.Subject)
async def get_subject(subject_id: int, db=Depends(get_db)):
    return util.get_subject(subject_id, db)


@subject.get('/', response_model=List[schemas.Subject])
async def get_subjects(db=Depends(get_db)):
    return util.get_subjects(db)


@subject.post('/')
async def add_subject(subject: schemas.SubjectCreate, db=Depends(get_db)):
    return util.add_subject(subject, db)


@subject.put('/{subject_id}', response_model=schemas.Subject)
async def update_subject(subject_id: int, new_name: str, db=Depends(get_db)):
    return util.update_subject(subject_id, new_name, db)


@subject.delete('/{subject_id}', response_model=schemas.Subject)
async def delete_subject(subject_id: int, db=Depends(get_db)):
    return util.delete_subject(subject_id, db)


@subject.get('/{subject_id}/projects', response_model=schemas.Project)
async def get_projects_from_subject(subject_id: int, db=Depends(get_db)):
    return util.get_projects_from_subject(subject_id, db)


@study.get('/{study_id}', response_model=schemas.Study)
async def get_study(study_id: int, db=Depends(get_db)):
    return util.get_study(study_id, db)


@study.get('/', response_model=List[schemas.Study])
async def get_studies(db=Depends(get_db)):
    return util.get_studies(db)


@study.post('/')
async def add_study(study: schemas.SubjectCreate, db=Depends(get_db)):
    return util.add_study(study, db)


@study.delete('/{study_id}', response_model=schemas.Study)
async def delete_subject(study_id: int, db=Depends(get_db)):
    return util.delete_subject(study_id, db)
