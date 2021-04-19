from pydantic import BaseModel
from typing import Optional, List


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
    scopes: List[str] = []


class Role(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class Permission(BaseModel):
    id: int
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
