from fastapi import APIRouter

from app.api import photos, reports, signatures, tasks

api_router = APIRouter()
api_router.include_router(reports.router, prefix="/reports", tags=["reports"])
api_router.include_router(photos.router, prefix="/photos", tags=["photos"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
api_router.include_router(signatures.router, prefix="/signatures", tags=["signatures"])
