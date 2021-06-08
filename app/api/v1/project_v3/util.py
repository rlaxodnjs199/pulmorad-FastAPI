from sqlalchemy.orm import Session
from . import models, schemas


def get_project(project_id: int, db: Session):
    return db.query(models.Project).get(project_id)


def add_project(new_project: schemas.ProjectCreate, db: Session):
    project = models.Project(name=new_project.name)
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


def update_project(project_id: int, new_name: str, db: Session):
    project = db.query(models.Project).get(project_id)
    project.name = new_name
    db.commit()
    db.refresh(project)
    return project


def delete_project(project_id: int, db: Session):
    project = db.query(models.Project).get(project_id)
    db.delete(project)
    db.commit()
    return project
