
from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import models, schemas


def save_image(db: Session, image: schemas.Image):
    return


def get_subject(db: Session, subject_id: int):
    return db.query(models.Subject).filter(models.Subject.id == subject_id).first()


def create_subject(db: Session, subject: schemas.Subject):
    db_subject = models.Subject(name=subject.name)
    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)
    return db_subject


def get_subject_images(db: Session, subject_id: int):
    subject = db.query(models.Subject).filter(
        models.Subject.id == subject_id).first()
    subject_images = list(map(lambda image: image.url, subject.images))
    return subject_images


def post_subject_images(db: Session, subject_id: int, image_urls: List[str]):
    subject = get_subject(db, subject_id)
    try:
        for url in image_urls:
            db_image = models.Image(url=url, subject_name=subject.name)
            db.add(db_image)
            db.commit()
            db.refresh(db_image)
    except:
        raise HTTPException(
            status_code=400, detail="Error adding images to DB")
