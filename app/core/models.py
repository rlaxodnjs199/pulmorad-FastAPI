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
                           Column('user_id', UUID, ForeignKey('user.id')),
                           Column(
                               'role_id', Integer, ForeignKey('role.id')
                           ))


class Role(Base):
    __tablename__ = "role"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20), unique=True)
    description = Column(String(20), nullable=True)
    permissions = relationship(
        "Permission", secondary=role_to_permission_table)


class Permission(Base):
    __tablename__ = "permission"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20), unique=True)
    description = Column(String(20), nullable=True)


# class UserToRole(Base):
#     __tablename__ = "user_to_role"

#     user_id = Column(Integer)
#     role_id = Column(Integer)


# class Project(Base):
#     __tablename__ = "project"

#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, unique=True, index=True)

#     studies = relationship("Study", back_populates="project")


# class Study(Base):
#     __tablename__ = "study"

#     id = Column(Integer, primary_key=True, index=True)
#     instance_uid = Column(String(100), unique=True, index=True)
#     access_number = Column(String(50), nullable=True)
#     patient_id = Column(String(40), nullable=False)
#     patient_name = Column(String(40), nullable=False)
#     study_date = Column(String(15), nullable=True)
#     study_description = Column(String(50), nullable=True)
#     modalities = Column(String(20), nullable=True)
#     project_title = Column(String(20), ForeignKey("project.title"))

#     project = relationship("Project", back_populates="studies")
