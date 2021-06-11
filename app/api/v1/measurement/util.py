from typing import Dict, List
from sqlalchemy.orm import Session
from . import models, schemas

def get_all_measurements(db: Session):
    return db.query(models.Measurement).all()



def create_measurement(db: Session, measurement: List[schemas.Measurement]):
    print('CREATE MEASUREMENT STARTS...')
    response = []
    
    # check if there is a duplicate
    study_list = list(map(lambda x: x.StudyInstanceUID, measurement))
    patient_list = list(map(lambda x: x.PatientID, measurement))
    series_list = list(map(lambda x: x.SeriesInstanceUID, measurement))
    _patient = list(dict.fromkeys(patient_list))
    _study = list(dict.fromkeys(study_list))
    _series = list(dict.fromkeys(series_list))
    
    if (len(_patient) != 1 or len(_study) != 1 or len(_series)):
        raise Exception('Save measurement only can save same Patient, Study, and Series')

    # delete previous data that is in the same series.
    db.query(models.Measurement).filter_by(PatientID=_patient[0], StudyInstanceUID=_study[0], SeriesInstanceUID=_series[0]).delete()

    # db.query.filter_by()

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
            rAngle=measure.rAngle
        )
        db.add(db_measurements)
        db.commit()
        db.refresh(db_measurements)
        response.append(db_measurements)
    return response
