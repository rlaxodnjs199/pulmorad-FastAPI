import os
import uuid
from sqlalchemy.dialects.postgresql import UUID
from os.path import join, dirname
from typing import Optional

from sqlalchemy import Table, Column, Integer,  String, Boolean
from passlib.context import CryptContext
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import inspect
from sqlalchemy.engine import Engine

from app import config
from app.db import models
from app.db.util.guid_type import setup_guids_postgresql


db_engine = create_engine(str(config.DATABASE_URL))
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
models.Base.metadata.create_all(bind=db_engine)


def add_user_to_db(db_engine: Engine, username: str, hashed_password: str, role: str, is_active: bool, is_superuser: bool):
    engine = db_engine
    engine_inspect = inspect(engine)

    if 'users' not in engine_inspect.get_table_names():
        print('users table does not exists!')
        return

    conn = engine.connect()

    user_table = Table('users', MetaData(), autoload=True,
                       autoload_with=conn, postgresql_ignore_search_path=True)
    user_table_insert = user_table.insert().values(
        id=uuid.uuid4().hex,
        username=username,
        hashed_password=hashed_password,
        role=role,
        is_active=is_active,
        is_superuser=is_superuser
    )

    conn.execute(user_table_insert)


def add_user(username: str, password: str, role: str = 'user', is_active: bool = True, is_superuser: bool = False, full_name: Optional[str] = None, email: Optional[str] = None):
    hashed_password = pwd_context.hash(password)
    add_user_to_db(db_engine, username, hashed_password,
                   role, is_active, is_superuser)


#add_user('inq', 'clsrn123')
#update_password('twkim', 'clsrn123')
#query_result = query_user(engine, 'twkim')
