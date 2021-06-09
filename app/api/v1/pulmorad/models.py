from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.pgsql.base_model import Base


class Project(Base):
    __tablename__ = "project"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True)

    studies = relationship("Study", back_populates="project")


class Study(Base):
    __tablename__ = "study"

    id = Column(Integer, primary_key=True, index=True)
    instance_uid = Column(String(100), unique=True, index=True)
    access_number = Column(String(50), nullable=True)
    patient_id = Column(String(40), nullable=False)
    patient_name = Column(String(40), nullable=False)
    study_date = Column(String(15), nullable=True)
    study_description = Column(String(50), nullable=True)
    modalities = Column(String(20), nullable=True)
    project_title = Column(String(20), ForeignKey("project.title"))

    project = relationship("Project", back_populates="studies")
