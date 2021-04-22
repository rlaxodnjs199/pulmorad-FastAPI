from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import SecurityScopes
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from app.db.pgsql.session import get_db
from app.api.v1.user.util import get_user_by_username, get_permissions_from_user
from app.api.v1.user.schemas import UserFromDB
from .security import verify_password


def authenticate_user(db, username: str, password: str) -> Optional[UserFromDB]:
    user = get_user_by_username(db, username)

    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def validate_user_permission(security_scopes: SecurityScopes, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    Authorize.jwt_required()
    username = Authorize.get_jwt_subject()

    permission_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Operation Not Permitted',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        user_id = get_user_by_username(db, username).id
        permissions = get_permissions_from_user(db, user_id)
        print(permissions)
        print(security_scopes.scopes)
        for scope in security_scopes.scopes:
            if scope not in permissions:
                raise permission_error
    except:
        raise permission_error


def get_username_from_jwt(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()

    return Authorize.get_jwt_subject()
