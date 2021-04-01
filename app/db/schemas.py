from pydantic import BaseModel
from typing import Optional


class UserBase(BaseModel):
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    role: str = 'user'


class UserFromDB(UserBase):
    hashed_password: str


class UserCreate(UserBase):
    password: str

    class Config:
        orm_mode = True
