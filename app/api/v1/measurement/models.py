from sqlalchemy import Boolean, Column, Integer, Float, String, ForeignKey, JSON
from sqlalchemy.orm import relationship

from app.db.pgsql.base_model import Base



class Measurement(Base):
    __tablename__ = "measurement"
    
    id=Column(String, primary_key=True)
    PatientID=Column(String)
    SOPInstanceUID=Column(String)
    SeriesInstanceUID=Column(String)
    StudyInstanceUID=Column(String)
    active=Column(Boolean)
    color=Column(String)
    frameIndex=Column(Integer)
    start=Column(String)
    middle=Column(String)
    end=Column(String)
    textBox=Column(String)
    
    userId=Column(String)
    # invalidated: bool
    lesionNamingNumber=Column(Integer)
    measurementNumber=Column(Integer)
    text=Column(String)
    timepointId=Column(String)
    toolType=Column(String)
    visible=Column(Boolean)
    description=Column(String)
    location=Column(String)
    # Length
    unit=Column(String)
    # Angle
    rAngle=Column(Float)

    perpendicularEnd=Column(String)
    perpendicularStart=Column(String)
    isCreating=Column(Boolean)
    shortestDiameter=Column(Float)
    longestDiameter=Column(Float)