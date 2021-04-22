from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, Table, PrimaryKeyConstraint
from sqlalchemy.orm import relationship

from app.db.pgsql.base_model import Base

user_to_role_table = Table('user_to_role', Base.metadata,
                           Column('user_id', Integer,
                                  ForeignKey('user.id'), primary_key=True),
                           Column('role_id', Integer,
                                  ForeignKey('role.id'), primary_key=True))

role_to_permission_table = Table('role_to_permission', Base.metadata,
                                 Column('role_id', Integer,
                                        ForeignKey('role.id'), primary_key=True),
                                 Column('permission_id', Integer,
                                        ForeignKey('permission.id'), primary_key=True))


class User(Base):
    __tablename__ = "user"

    # id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    def __repr__(self):
        return "<User(username='%s', first_name='%s', last_name='%s')>" % (self.username, self.first_name, self.last_name)


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
