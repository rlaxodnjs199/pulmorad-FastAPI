from app.api.v1.user.schemas import UserCreate
from app.api.v1.user.models import User
from app.core.security import get_password_hash
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from . import models, schemas


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


def assign_permissions_to_role(db: Session, permission: schemas.Permission, role: schemas.Role):
    try:
        statement = models.role_to_permission_table.insert().values(
            role_id=role.id, permission_id=permission.id)
        db.execute(statement)
        db.commit()
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid role ID or permission ID',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    return {'msg': 'success'}


def assign_role_to_user(db: Session, role: schemas.Role, userID):
    try:
        statement = models.user_to_role_table.insert().values(
            user_id=userID, role_id=role.id
        )
        db.execute(statement)
        db.commit()
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid user ID or role ID',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    return {'msg': 'success'}
