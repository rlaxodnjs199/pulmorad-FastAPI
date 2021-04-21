from app.api.v1.user.schemas import UserCreate
from app.api.v1.user.models import User
from app.core.security import get_password_hash
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from . import models, schemas
from app.core.models import Role, Permission


def create_role(db: Session, role: schemas.RoleCreate):
    try:
        role_to_add = models.Role(
            name=role.name,
            description=role.description
        )
        db.add(role_to_add)
        db.commit()
        db.refresh(role_to_add)
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid role name',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    return role_to_add


def create_permission(db: Session, permission: schemas.PermissionCreate):
    try:
        permission_to_add = models.Permission(
            name=permission.name,
            description=permission.description
        )
        db.add(permission_to_add)
        db.commit()
        db.refresh(permission_to_add)
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid role name',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    return permission_to_add


def add_permissions_to_role(db: Session, role_id, permission_id):
    try:
        role = db.query(models.Role).get(role_id)
        permission = db.query(models.Permission).get(permission_id)
        permission.roles.append(role)
        db.add(permission)
        db.commit()
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid role ID or permission ID',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    return {'msg': 'success'}


def add_roles_to_user(db: Session, user_id, role_id):
    try:
        user = db.query(models.User).get(user_id)
        role = db.query(models.Role).get(role_id)
        role.users.append(user)
        db.add(role)
        db.commit()
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid user ID or role ID',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    return {'msg': 'success'}


def get_permissions_from_user(db: Session, user_id):
    try:
        user = db.query(models.User).get(user_id)
        roles = user.roles
        permissions = []
        for role in roles:
            for permission in role.permissions:
                permissions.append(permission.name)
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid user ID',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    return permissions
