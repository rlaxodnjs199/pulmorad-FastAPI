from typing import List, Dict
from fastapi import Depends, APIRouter, HTTPException, status

from app.db.pgsql.session import get_db
from . import schemas, util

project_router = project = APIRouter()


@project.get('/initgrid/')
async def get_initial_rendering_data(db=Depends(get_db)):
    return util.get_initial_rendering_data(db=db)


@project.get('/projects/', response_model=List[schemas.Project])
async def get_project_list(db=Depends(get_db)):
    return util.get_projects(db=db)


@project.post('/projects/', response_model=schemas.Project)
async def add_project(project_create: schemas.ProjectCreate, db=Depends(get_db)):
    print(project_create)
    return util.create_project(db, project_create)


@project.get('/projects/{project_title}', response_model=schemas.Project)
async def get_project_by_title(project_title: str, db=Depends(get_db)):
    db_project = util.get_project_by_title(db, project_title)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project


@project.get('/projects/{project_id}', response_model=schemas.Project)
async def get_project_by_id(project_id: int, db=Depends(get_db)):
    db_project = util.get_project_by_id(db, project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project


@project.get('/studies/')
async def get_study_by_project_title(db=Depends(get_db)):
    return util.get_study_by_project_title_dict(db)


@project.post('/studies/', response_model=List[schemas.Study])
async def create_study_for_project(studies: List[schemas.Study], db=Depends(get_db)):
    return util.create_studies(db, studies)
