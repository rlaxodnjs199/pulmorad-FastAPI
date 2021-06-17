from typing import List, Dict
from fastapi import Depends, APIRouter, HTTPException, status

from app.db.pgsql.session import get_db
from . import schemas, util

measurement_router = measurement = APIRouter()

@measurement.get('/measurements/', response_model=List[schemas.Measurement])
async def get_all_measurements(db=Depends(get_db)):
    return util.get_all_measurements(db)


# @measurement.get('/measurements/{measurement_id}', response_model=schemas.Measurement)
# async def get_measurement_by_id(measurement_id: str, db=Depends(get_db)):
#     db_measurement = util.get_measurement_by_id(db, measurement_id)
#     if db_measurement is None:
#         raise HTTPException(status_code=404, detail="Measurement not found")
#     return db_measurement

# @measurement.post('/measurements/', response_model=schemas.Measurement)
# async def add_measurement(measurement: List[schemas.Measurement], db=Depends(get_db)):
#     print('create all measurements', measurement)
#     return util.create_measurement(db, measurement)


@measurement.post('/measurements/{patient_id}', response_model=List[schemas.Measurement])
async def add_measurement(patient_id: str, measurement: List[schemas.Measurement], db=Depends(get_db)):
    print(f'create all measurements for {patient_id}', measurement)
    return util.create_measurement(db, measurement, patient_id)
