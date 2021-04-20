from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
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
