from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.pgsql.base_model import Base


project_subject_association_table = Table('project_subject_association', Base.metadata, Column('project_id', Integer, ForeignKey(
    'project.id'), primary_key=True), Column('subject_id', Integer, ForeignKey('subject.id'), primary_key=True))


class Project(Base):
    __tablename__ = 'project'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20), unique=True, index=True, nullable=False)
    date_created = Column(DateTime, server_default=func.now())
    date_updated = Column(DateTime, onupdate=func.now())
    description = Column(String)

    subjects = relationship(
        'Subject', secondary=project_subject_association_table, back_populates='projects')

    def __repr__(self) -> str:
        return "<Project(id='%d', name='%s')>" % (self.id, self.name)


class Subject(Base):
    __tablename__ = 'subject'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20), unique=True, index=True, nullable=False)
    date_created = Column(DateTime, server_default=func.now())
    date_updated = Column(DateTime, onupdate=func.now())

    projects = relationship(
        'Project', secondary=project_subject_association_table, back_populates='subjects')

    studies = relationship('Study')

    def __repr__(self) -> str:
        return "<Subject(id='%d', name='%s')>" % (self.id, self.name)


class Study(Base):
    __tablename__ = 'study'

    id = Column(Integer, primary_key=True, index=True)
    accession_number = Column(String, nullable=False)
    sop_instance_uid = Column(String, nullable=False)
    series_instance_uid = Column(String, nullable=False)
    study_instance_uid = Column(String, nullable=False)
    study_date = Column(String(15), nullable=False)
    date_created = Column(DateTime, server_default=func.now())
    date_updated = Column(DateTime, onupdate=func.now())

    subject = relationship('Subject', ForeignKey('Subject.id'))

    def __repr__(self) -> str:
        return "<Study(accession_number ='%s')>" % (self.accession_number)
