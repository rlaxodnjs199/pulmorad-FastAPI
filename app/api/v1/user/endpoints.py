from typing import List

from fastapi import APIRouter, Depends, Security
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from app.db.pgsql.session import get_db
from app.core.util import validate_user_permission, get_username_from_jwt
from . import models, schemas, util

user_router = user = APIRouter()


@user.get('/users/me')
def get_current_user_name(username: str = Depends(get_username_from_jwt)):
    return {"username": username}


@user.get('/users/profile', response_model=schemas.User)
def get_current_user_info(username: str = Depends(get_username_from_jwt), db: Session = Depends(get_db)):
    return util.get_user_by_username(db, username)


@user.post('/users', response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return util.create_user(db, user)


@user.get('/roles', response_model=List[schemas.Role])
def get_roles(db: Session = Depends(get_db)):
    roles = db.query(models.Role).all()
    return roles


@user.post('/roles', response_model=schemas.Role)
def create_roles(role: schemas.RoleCreate, db: Session = Depends(get_db)):
    return util.create_role(db, role)


@user.get('/permissions', response_model=List[schemas.Permission])
def get_permissions(db: Session = Depends(get_db)):
    permissions = db.query(models.Permission).all()
    return permissions


@user.post('/permissions', response_model=schemas.Permission)
def create_permission(permission: schemas.PermissionCreate, db: Session = Depends(get_db)):
    return util.create_permission(db, permission)


@user.post('/roles/{role_id}/permissions/{permission_id}')
def assign_permissions_to_role(role_id: int, permission_id: int, db: Session = Depends(get_db)):
    return util.assign_permission_to_role(db, role_id, permission_id)


@user.post('/users/{user_id}/roles/{role_id}')
def assign_role_to_user(user_id: int, role_id: int, db: Session = Depends(get_db)):
    return util.assign_role_to_user(db, user_id, role_id)


@user.get('/users/{user_id}/permissions')
def get_user_permissions(user_id: int, db: Session = Depends(get_db)):
    return util.get_permissions_from_user(db, user_id)
