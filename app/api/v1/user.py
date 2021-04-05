from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT

from app.db.session import get_db

user_router = user = APIRouter()


@user.get('/user')
def get_user(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()

    current_user = Authorize.get_jwt_subject()
    return {"user": current_user}
