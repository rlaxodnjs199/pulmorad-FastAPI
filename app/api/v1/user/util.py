from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.api.v1.user.models import User
from app.api.v1.user.schemas import UserCreate


def get_user(db: Session, user_id: int) -> User:
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
