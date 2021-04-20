from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, Table
from sqlalchemy.orm import relationship

from app.db.pgsql.base_model import Base
from app.api.v1.user.models import User


role_to_permission_table = Table('role_to_permission', Base.metadata,
                                 Column('role_id', Integer,
                                        ForeignKey('role.id')),
                                 Column('permission_id', Integer, ForeignKey('permission.id')))

user_to_role_table = Table('user_to_role', Base.metadata,
                           Column('user_id', Integer, ForeignKey('user.id')),
                           Column(
                               'role_id', Integer, ForeignKey('role.id')
                           ))


class Role(Base):
    __tablename__ = "role"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20), unique=True)
    description = Column(String(20), nullable=True)
    users = relationship("User", secondary=user_to_role_table,
                         backref="roles", lazy="dynamic")
    permissions = relationship(
        "Permission", secondary=role_to_permission_table, backref="roles", lazy="dynamic")


class Permission(Base):
    __tablename__ = "permission"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20), unique=True)
    description = Column(String(20), nullable=True)
