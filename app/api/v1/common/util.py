from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import mode
from . import models, schemas


def get_project(project_id: int, db: Session):
    return db.query(models.Project).get(project_id)


def get_projects(db: Session):
    return db.query(models.Project).all()


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


def get_subjects_from_project(project_id: int, db: Session):
    subjects = db.query(models.Project).get(project_id).subjects
    return subjects


def get_subject(subject_id: int, db: Session):
    return db.query(models.Subject).get(subject_id)


def get_subjects(db: Session):
    return db.query(models.Subject).all()


def add_subject(new_subject: schemas.SubjectCreate, db: Session):
    subject = models.Subject(name=new_subject.name)
    db.add(subject)
    db.commit()
    db.refresh(subject)
    return subject


def update_subject(subject_id: int, new_name: str, db: Session):
    subject = db.query(models.Subject).get(subject_id)
    subject.name = new_name
    db.commit()
    db.refresh(subject)
    return subject


def delete_subject(subject_id: int, db: Session):
    subject = db.query(models.Subject).get(subject_id)
    db.delete(subject)
    db.commit()
    return subject


def get_projects_from_subject(subject_id: int, db: Session):
    projects = db.query(models.Subject).get(subject_id).projects
    return projects


def assign_subject_to_project(project_id: int, subject_id: int, db: Session):
    project = db.query(models.Project).get(project_id)
    subject = db.query(models.Subject).get(subject_id)
    project.subjects.append(subject)
    db.add(project)
    db.commit()
    return {'msg': f'Assign Subject:{subject.name} to project:{project.name} Success'}


def unassign_subject_from_project(project_id: int, subject_id: int, db: Session):
    project = db.query(models.Project).get(project_id)
    subject = db.query(models.Subject).get(subject_id)
    project.subjects.remove(subject)
    db.add(project)
    db.commit()
    return {'msg': f'Unassign Subject:{subject.name} from project:{project.name} Success'}
