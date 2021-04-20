from typing import Optional, List
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
from app.api.v1.user.schemas import UserFromDB, User
from app.api.v1.user.util import get_user_by_username
from . import models, schemas, util


auth_router = auth = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login", scopes={
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


def get_current_user(security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme), Authorize: AuthJWT = Depends()):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
        print(authenticate_value)
    else:
        authenticate_value = f"Bearer"
        print(authenticate_value)
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        jwt = Authorize.get_raw_jwt(token)
        subject = jwt['sub']
        scopes = jwt['scopes']
        print(subject)
        print(scopes)
    except:
        raise credentials_exception
    return subject


async def get_current_active_user(current_user: User = Security(get_current_user, scopes=["me"])):
    return current_user


@auth.get("/me/")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@auth.get('/', response_model=schemas.TokenData)
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
    # permission = await redis.get(authorization)

    return {'username': username, 'scopes': []}


@auth.post('/login', response_model=schemas.Token)
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


@auth.get('/roles', response_model=List[schemas.Role])
def get_roles(db: Session = Depends(get_db)):
    roles = db.query(models.Role).all()
    return roles


@auth.get('/permissions', response_model=schemas.Permission)
def get_permissions(db: Session = Depends(get_db)):
    permissions = db.query(models.Permission).all()
    return permissions


@auth.post('/roles', response_model=schemas.Role)
def create_roles(role: schemas.RoleCreate, db: Session = Depends(get_db)):
    return util.create_role(db, role)


@auth.post('/permissions', response_model=schemas.Permission)
def create_permission(permission: schemas.PermissionCreate, db: Session = Depends(get_db)):
    return util.create_permission(db, permission)


@auth.post('/permissions/assign')
def assign_permissions_to_role(role_id: int, permission_id: int, db: Session = Depends(get_db)):
    return util.add_permissions_to_role(db, role_id, permission_id)


@auth.post('/role/assign')
def assign_role_to_user(user_id: int, role_id: int, db: Session = Depends(get_db)):
    return util.add_roles_to_user(db, user_id, role_id)


@auth.get('/get_user_permissions')
def get_user_permissions(user_id: int, db: Session = Depends(get_db)):
    return util.get_permissions_from_user(db, user_id)
