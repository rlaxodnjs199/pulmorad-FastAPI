from typing import Optional
from fastapi import Depends, APIRouter, HTTPException, status, Request, Security
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, SecurityScopes
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app import config
from app.core.settings import get_JWT_settings
from app.core.security import verify_password
from app.db.pgsql.session import get_db
from app.db.redis.session import redis
from app.api.v1.user.models import User
from app.api.v1.user.schemas import UserFromDB, UserBase
from app.api.v1.user.util import get_user_by_username


import jwt

auth_router = auth = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login", scopes={
                                     "me": "Read information about the current user.", "items": "Read items."},)


@AuthJWT.load_config
def load_JWT_settings():
    return get_JWT_settings()


def authenticate_user(db_engine, username: str, password: str) -> Optional[UserFromDB]:
    user = get_user_by_username(db_engine, username)

    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


@auth.get('/')
async def check_auth(request: Request, Authorize: AuthJWT = Depends()):
    authorization: Optional[str] = request.cookies.get("access_token_cookie")

    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='No authorization',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    jwt = Authorize.jwt_required()
    username = Authorize.get_jwt_subject()
    permission = await redis.get(authorization)

    return {'username': username, 'permission': permission}


@auth.post('/login')
async def login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends(), Authorize: AuthJWT = Depends()):
    user = authenticate_user(db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    access_token = Authorize.create_access_token(
        subject=form_data.username, user_claims={"scopes": form_data.scopes})
    refresh_token = Authorize.create_refresh_token(subject=form_data.username)
    # Set the JWT cookies in the response
    Authorize.set_access_cookies(access_token)
    Authorize.set_refresh_cookies(refresh_token)
    # Set Cookie: Permission in Redis
    await redis.set(access_token, 'user')

    return {"access_token": access_token, "token_type": "bearer"}


@auth.post('/refresh')
def refresh(Authorize: AuthJWT = Depends()):
    Authorize.jwt_refresh_token_required()

    current_user = Authorize.get_jwt_subject()
    new_access_token = Authorize.create_access_token(subject=current_user)
    # Set the JWT and CSRF double submit cookies in the response
    Authorize.set_access_cookies(new_access_token)

    return {"msg": "The token has been refresh"}


@auth.delete('/logout')
def logout(request: Request, Authorize: AuthJWT = Depends()):
    # Authorize.jwt_required()
    # redis.delete()
    # Redis unset Key
    Authorize.unset_jwt_cookies()

    return {"msg": "Successfully logout"}


# async def get_current_user(Authorize: AuthJWT = Depends()):
#     user =
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid authentication credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     return user

# @auth.get('/user/me')
# async def read_users_me(current_user: UserBase = Depends(get_current_active_user)):
#     return current_user

# async def get_current_user(security_scopes: SecurityScopes, token):


# async def get_current_active_user(current_user: User = Security(get_current_user, scopes=["me"])):
#     return current_user

# def verify_scopes(current_user, scopes):


@auth.get('/user')
def user(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()

    current_user = Authorize.get_jwt_subject()
    scopes = Authorize.get_raw_jwt()['scopes']

    # if verify_scopes():

    return {"user": current_user, 'scopes': scopes}
