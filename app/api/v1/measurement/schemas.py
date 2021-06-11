from typing import Optional, List, Dict
from pydantic import BaseModel


class Measurement(BaseModel):
    id: str
    PatientID: str
    SOPInstanceUID: str
    SeriesInstanceUID: str
    StudyInstanceUID: str
    active: Optional[bool]
    color: Optional[str]
    frameIndex: Optional[int]
    start: Optional[str]
    middle: Optional[str]
    end: Optional[str]
    
    userId: Optional[str]
    # invalidated: bool
    lesionNamingNumber: Optional[int]
    measurementNumber: Optional[int]
    text: Optional[str]
    timepointId: Optional[str]
    toolType: Optional[str]
    visible: Optional[bool]
    description: Optional[str]
    location: Optional[str]
    # Length
    unit: Optional[str]
    # Angle
    rAngle: Optional[float]
    class Config:
        orm_mode = True



# class Measurement(BaseModel):
        
#     FrameOfReferenceUID: str
#     SOPInstanceUID: str                #   "1.3.12.2.1107.5.1.4.55301.30000020092813472264000004919"
#     area:str                          #   undefined
#     description:str                   #   undefined
#     id:str                            #   "b6c02064-b14d-c0b5-7bda-81f4b58e5627"
#     label:str                         #   undefined
#     modifiedTimestamp:str             #   1622704484
#     points:str                        #   Array(2)
#     # 0: {x: 146.70370370370372, y: 63.2098765432099}
#     # 1: {x: 100.08641975308643, y: 476.44444444444457}
#     length:str                        #   2
#     referenceSeriesUID:str           #   "1.3.12.2.1107.5.1.4.55301.30000020092813472264000004920"
#     source:str
#     # source= Column(String(100), nullable=False)                       #   {id: "42424da2-419f-4ff7-52c3-b79cf8e376c2", name: "CornerstoneTools", version: "4", addOrUpdate: ƒ, getAnnotation: ƒ}
#     type:str                          #   "value_type::point"
#     unit:str                         #   undefined
