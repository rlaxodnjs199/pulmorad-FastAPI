from typing import Optional

from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from pydantic import BaseModel
from aioredis import Redis

from app import config
from app.db.session import get_db
from app.core.security import verify_password
from app.db.util.user import get_user_by_username
from app.db.schemas import UserFromDB
from app.db.models import User
from app.db.redis.session import init_redis_pool, insert_key, get_key


auth_router = auth = APIRouter()


class JWT_Settings(BaseModel):
    authjwt_secret_key: str = config.SECRET_KEY
    authjwt_token_location: set = {"cookies"}
    authjwt_cookie_csrf_protect: bool = True
    authjwt_cookie_samesite: str = 'lax'


@AuthJWT.load_config
def get_JWT_config():
    return JWT_Settings()


def get_redis_session():
    yield from init_redis_pool()


def authenticate_user(db_engine, username: str, password: str) -> Optional[UserFromDB]:
    user = get_user_by_username(db_engine, username)

    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


@auth.get('/auth')
async def check_auth(Authorize: AuthJWT = Depends()):
    jwt = Authorize.jwt_required()
    subject = Authorize.get_jwt_subject()
    print(subject)
    # key = 'hi'
    # value = 'bye'
    # print(redis_conn)
    # waited_value = await insert_key(redis_conn, key, value)
    # print(waited_value)
    return {'insert into redis': 'succeed'}


@auth.post('/login')
async def login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends(), Authorize: AuthJWT = Depends()):
    user = authenticate_user(db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    access_token = Authorize.create_access_token(subject=form_data.username)
    refresh_token = Authorize.create_refresh_token(subject=form_data.username)
    # Set the JWT cookies in the response
    Authorize.set_access_cookies(access_token)
    Authorize.set_refresh_cookies(refresh_token)
    # Set Cookie: Permission in Redis
    # insert_key(redis, access_token, 'user')
    # value = await get_key(redis, access_token)
    # print(value)

    return {"access_token": access_token, "username": user.username}


@auth.post('/refresh')
def refresh(Authorize: AuthJWT = Depends()):
    Authorize.jwt_refresh_token_required()

    current_user = Authorize.get_jwt_subject()
    new_access_token = Authorize.create_access_token(subject=current_user)
    # Set the JWT and CSRF double submit cookies in the response
    Authorize.set_access_cookies(new_access_token)
    return {"msg": "The token has been refresh"}


@auth.delete('/logout')
def logout(Authorize: AuthJWT = Depends()):
    # Authorize.jwt_required()

    Authorize.unset_jwt_cookies()
    return {"msg": "Successfully logout"}
