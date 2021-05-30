import re
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

from app.db.pgsql.base_model import Base


class Subject(Base):
    __tablename__ = 'subject'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    images = relationship("Image", back_populates="subject")


class Image(Base):
    __tablename__ = "subject_images"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, nullable=False)
    subject_name = Column(String(30), ForeignKey('subject.name'))

    subject = relationship("Subject", back_populates='images')
