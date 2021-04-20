# import uuid
# from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Boolean, Column, Integer, String

from app.db.pgsql.base_model import Base


class User(Base):
    __tablename__ = "user"

    #id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    def __repr__(self):
        return "<User(username='%s', first_name='%s', last_name='%s')>" % (self.username, self.first_name, self.last_name)
