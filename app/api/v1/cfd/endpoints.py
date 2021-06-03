from re import sub
from typing import List
from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse

from app.db.pgsql.session import get_db
from . import schemas, util

cfd_router = cfd = APIRouter()


@cfd.get('/subjects/{subject_id}')
async def get_subject(subject_id: int, db=Depends(get_db)):
    return util.get_subject(db, subject_id)


@cfd.post('/subjects')
async def create_subject(subject: schemas.SubjectCreate, db=Depends(get_db)):
    return util.create_subject(db, subject)


@cfd.get('/subjects/{subject_id}/images')
async def get_image_file(subject_id: int, db=Depends(get_db)):
    image_paths = util.get_subject_images(db, subject_id)
    return FileResponse(image_paths[1], media_type='image/png')


@cfd.post('/subjects/{subject_id}/images')
async def post_image_file(subject_id: int, image_urls: List[str], db=Depends(get_db)):
    return util.post_subject_images(db, subject_id, image_urls)
