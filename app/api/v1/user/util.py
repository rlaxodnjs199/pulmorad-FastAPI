from typing import List

from fastapi import HTTPException, status, Request, Depends
from fastapi.security import SecurityScopes
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.db.pgsql.session import get_db
from .models import User, Role, Permission
from .schemas import UserCreate, RoleCreate, PermissionCreate


def get_user_by_id(db: Session, user_id: int) -> User:
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    return user


def get_user_by_username(db: Session, username: str) -> User:
    user = db.query(User).filter(
        User.username == username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    return user


def create_user(db: Session, user: UserCreate):
    password = get_password_hash(user.password)

    try:
        user_to_add = User(
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            email=user.email,
            hashed_password=password,
        )
        db.add(user_to_add)
        db.commit()
        db.refresh(user_to_add)
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid username',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    return user_to_add


def create_role(db: Session, role: RoleCreate):
    try:
        role_to_add = Role(
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


def create_permission(db: Session, permission: PermissionCreate):
    try:
        permission_to_add = Permission(
            name=permission.name,
            description=permission.description
        )
        db.add(permission_to_add)
        db.commit()
        db.refresh(permission_to_add)
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid permission name',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    return permission_to_add


def assign_permission_to_role(db: Session, role_id: int, permission_id: int):
    try:
        role = db.query(Role).get(role_id)
        permission = db.query(Permission).get(permission_id)
        permission.roles.append(role)
        db.add(permission)
        db.commit()
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid role or permission Info',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    return {'msg': f'Assign permission:{permission.name} to role:{role.name} Success'}


def assign_role_to_user(db: Session, user_id: int, role_id: int):
    try:
        user = db.query(User).get(user_id)
        role = db.query(Role).get(role_id)
        role.users.append(user)
        db.add(role)
        db.commit()
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid user ID or role ID',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    return {'msg': f'Assign role:{role.name} to user:{user.username} Success'}


def get_permissions_from_user(db: Session, user_id: int) -> List[str]:
    try:
        user = db.query(User).get(user_id)
        roles = user.roles
        if roles:
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
