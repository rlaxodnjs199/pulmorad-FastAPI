from fastapi import APIRouter
from .common.endpoints import project_router, subject_router

api_router = APIRouter(prefix='/alveola')
api_router.include_router(project_router, tags=['project'])
api_router.include_router(subject_router, tags=['subject'])
