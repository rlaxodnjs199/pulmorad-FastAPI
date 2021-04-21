import functools
from typing import Optional, List
from fastapi import Depends, APIRouter, HTTPException, status, Request, Security
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestFormStrict, SecurityScopes
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app import config
from app.core.settings import get_JWT_settings
from app.core.security import verify_password
from app.db.pgsql.session import get_db
from app.db.redis.session import redis
from app.api.v1.user.models import User
from app.api.v1.user.schemas import UserFromDB, User
from app.api.v1.user.util import get_user_by_username
from . import models, schemas, util

auth_router = auth = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@ AuthJWT.load_config
def load_JWT_settings():
    return get_JWT_settings()


def authenticate_user(db_engine, username: str, password: str) -> Optional[UserFromDB]:
    user = get_user_by_username(db_engine, username)

    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def validate_user_permission(scopes_from_jwt: str, security_scopes: SecurityScopes) -> bool:
    jwt_scopes_set = set(scope for scope in scopes_from_jwt.split(' '))
    security_scopes_set = set(security_scopes)

    return (jwt_scopes_set >= security_scopes_set) and (jwt_scopes_set <= security_scopes_set)


def get_current_user(request: Request, security_scopes: SecurityScopes, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    try:
        Authorize.jwt_required()
        username = Authorize.get_jwt_subject()
        user = get_user_by_username(db, username)
        scopes = Authorize.get_raw_jwt()['scopes']

        if not validate_user_permission(scopes, security_scopes.scopes):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Scope validation failed',
                headers={'WWW-Authenticate': 'Bearer'},
            )
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": 'Bearer'},
        )

    return user


async def get_current_active_user(current_user: User = Security(get_current_user, scopes=["me:view"])):
    return current_user


@ auth.get("/user/me")
async def read_users_me(current_user: User = Security(get_current_active_user, scopes=["me:edit"])):
    return current_user


@ auth.get('/check-auth', response_model=schemas.TokenData)
async def check_auth(request: Request, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    Authorize.jwt_required()
    username = Authorize.get_jwt_subject()
    user_id = get_user_by_username(db, username).id
    permissions = util.get_permissions_from_user(db, user_id)

    return {'username': username, 'scopes': permissions}


@ auth.post('/login', response_model=schemas.Token)
async def login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestFormStrict = Depends(), Authorize: AuthJWT = Depends()):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    scopes = util.get_permissions_from_user(db, user.id)
    str_scopes = ' '.join(scopes)

    access_token = Authorize.create_access_token(
        subject=form_data.username, user_claims={"scopes": str_scopes})
    refresh_token = Authorize.create_refresh_token(subject=form_data.username)
    # Set the JWT cookies in the response
    Authorize.set_access_cookies(access_token)
    Authorize.set_refresh_cookies(refresh_token)
    # Set Cookie: Permission in Redis
    # await redis.set(access_token, 'user')

    return {"access_token": access_token, "token_type": "bearer"}


@ auth.post('/refresh')
def refresh(Authorize: AuthJWT = Depends()):
    Authorize.jwt_refresh_token_required()

    current_user = Authorize.get_jwt_subject()
    new_access_token = Authorize.create_access_token(subject=current_user)
    # Set the JWT and CSRF double submit cookies in the response
    Authorize.set_access_cookies(new_access_token)

    return {"msg": "The token has been refresh"}


@ auth.delete('/logout')
def logout(request: Request, Authorize: AuthJWT = Depends()):
    # Authorize.jwt_required()
    # redis.delete()
    # Redis unset Key
    Authorize.unset_jwt_cookies()

    return {"msg": "Successfully logout"}


@ auth.get('/roles', response_model=List[schemas.Role])
def get_roles(db: Session = Depends(get_db)):
    roles = db.query(models.Role).all()
    return roles


@ auth.get('/permissions', response_model=List[schemas.Permission])
def get_permissions(db: Session = Depends(get_db)):
    permissions = db.query(models.Permission).all()
    return permissions


@ auth.post('/roles', response_model=schemas.Role)
def create_roles(role: schemas.RoleCreate, db: Session = Depends(get_db)):
    return util.create_role(db, role)


@ auth.post('/permissions', response_model=schemas.Permission)
def create_permission(permission: schemas.PermissionCreate, db: Session = Depends(get_db)):
    return util.create_permission(db, permission)


@ auth.post('/permissions/assign')
def assign_permissions_to_role(role_id: int, permission_id: int, db: Session = Depends(get_db)):
    return util.add_permissions_to_role(db, role_id, permission_id)


@ auth.post('/role/assign')
def assign_role_to_user(user_id: int, role_id: int, db: Session = Depends(get_db)):
    return util.add_roles_to_user(db, user_id, role_id)


@ auth.get('/get_user_permissions')
def get_user_permissions(user_id: int, db: Session = Depends(get_db)):
    return util.get_permissions_from_user(db, user_id)
