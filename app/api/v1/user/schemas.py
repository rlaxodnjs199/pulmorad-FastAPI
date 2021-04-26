from pydantic import BaseModel
from typing import Optional, List


class User(BaseModel):
    id: int
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None

    class Config:
        orm_mode = True


class UserFromDB(User):
    hashed_password: str


class UserCreate(User):
    password: str

    class Config:
        orm_mode = True


class Role(BaseModel):
    name: str

    class Config:
        orm_mode = True


class Permission(BaseModel):
    name: str

    class Config:
        orm_mode = True


class RoleCreate(Role):
    description: Optional[str] = None

    class Config:
        orm_mode = True


class PermissionCreate(Permission):
    description: Optional[str] = None

    class Config:
        orm_mode = True
