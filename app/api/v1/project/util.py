from typing import Dict, List
from sqlalchemy.orm import Session
from . import models, schemas


def get_project_by_id(db: Session, project_id: int):
    return db.query(models.Project).filter(models.Project.id == project_id).first()


def get_project_by_title(db: Session, project_title: str):
    return db.query(models.Project).filter(models.Project.title == project_title).first()


def get_projects(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Project).offset(skip).limit(limit).all()


def get_project_titles(db: Session, skip: int = 0, limit: int = 100):
    projects = db.query(models.Project).offset(skip).limit(limit).all()
    project_titles = list(map(
        lambda project: project.title, projects))
    return project_titles


def create_project(db: Session, project_create: schemas.ProjectCreate):
    db_project = models.Project(title=project_create.title)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


def get_studies_by_project(db: Session, project_id: int):
    return db.query(models.Study).filter(models.Study.owner_id == project_id).all()


def get_initial_rendering_data(db: Session, skip: int = 0, limit: int = 100) -> List:
    studies = db.query(
        models.Study).offset(skip).limit(limit).all()
    study_by_project_title_dict = {
        study.instance_uid: study.project_title for study in studies}

    return [get_projects(db), study_by_project_title_dict]


def create_studies(db: Session, studies: List[schemas.Study]):
    response = []
    for study in studies:
        db_study = models.Study(instance_uid=study.instance_uid, access_number=study.access_number, project_title=study.project_title, modalities=study.modalities,
                                patient_id=study.patient_id, patient_name=study.patient_name, study_date=study.study_date, study_description=study.study_description)
        db.add(db_study)
        db.commit()
        db.refresh(db_study)
        response.append(db_study)
    return response
