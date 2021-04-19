from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT

from app.db.pgsql.session import get_db
from . import schemas, util

user_router = user = APIRouter()


@user.get('/me')
def get_current_user(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()

    current_user = Authorize.get_jwt_subject()
    return {"user": current_user}


@user.post('/', response_model=schemas.User)
def create_user(user: schemas.UserCreate, db=Depends(get_db)):
    return util.create_user(db, user)
