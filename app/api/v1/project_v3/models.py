from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.pgsql.base_model import Base


class Project(Base):
    __tablename__ = "project"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20), unique=True, index=True, nullable=False)
    date_created = Column(DateTime, server_default=func.now())
    date_updated = Column(DateTime, onupdate=func.now())
    description = Column(String)

    # subjects = relationship("Subject", back_populates=)
