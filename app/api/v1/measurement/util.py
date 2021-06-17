from typing import Dict, List
from sqlalchemy.orm import Session
from . import models, schemas

def get_all_measurements(db: Session):
    return db.query(models.Measurement).all()



def create_measurement(db: Session, measurement: List[schemas.Measurement], patient_id: str):
    print(f'CREATE MEASUREMENT STARTS... {len(measurement)} ...... for {patient_id}')
    response = []
    
    # # check if there is a duplicate
    # study_list = list(map(lambda x: x.StudyInstanceUID, measurement))
    # patient_list = list(map(lambda x: x.PatientID, measurement))
    # series_list = list(map(lambda x: x.SeriesInstanceUID, measurement))
    # _patient = list(dict.fromkeys(patient_list))
    # _study = list(dict.fromkeys(study_list))
    # _series = list(dict.fromkeys(series_list))
    
    # # First measurement save
    # print(f'PATIENT: {len(_patient)}      STUDY: {len(_study)}       SERIES: {len(_series)}')
    # if (len(_patient) == 0 and len(_study) == 0 and len(_series) == 0):
    #     pass
    # else:
    #     if (len(_patient) != 1 or len(_study) != 1 or len(_series) != 1):
    #         print(f'raising error ... PATIENT: {len(_patient)}      STUDY: {len(_study)}       SERIES: {len(_series)}')
    #         raise Exception('Save measurement only can save same Patient, Study, and Series')
    #     # delete previous data that is in the same series.
        
    print('deleting measurements...\n')  
    db.query(models.Measurement).filter_by(PatientID=patient_id).delete()


    for measure in measurement:
        print(f'{measure.PatientID} | {measure.SOPInstanceUID} || {measure.SeriesInstanceUID} ||| {measure.StudyInstanceUID} |||| {measure.frameIndex}\n')
        db_measurements = models.Measurement(
            id=measure.id,
            PatientID=measure.PatientID,
            SOPInstanceUID=measure.SOPInstanceUID,
            SeriesInstanceUID=measure.SeriesInstanceUID,
            StudyInstanceUID=measure.StudyInstanceUID,
            active=measure.active,
            color=measure.color,
            frameIndex=measure.frameIndex,
            start=measure.start,
            middle=measure.middle,
            end=measure.end,
            textBox=measure.textBox,
            userId=measure.userId,
            lesionNamingNumber=measure.lesionNamingNumber,
            measurementNumber=measure.measurementNumber,
            text=measure.text,
            timepointId=measure.timepointId,
            toolType=measure.toolType,
            visible=measure.visible,
            description=measure.description,
            location=measure.location,
            unit=measure.unit,
            rAngle=measure.rAngle,
            perpendicularEnd=measure.perpendicularEnd,
            perpendicularStart=measure.perpendicularStart,
            isCreating=measure.isCreating,
            shortestDiameter=measure.shortestDiameter,
            longestDiameter=measure.longestDiameter
        )
        db.add(db_measurements)
        db.commit()
        db.refresh(db_measurements)
        response.append(db_measurements)
    return response
