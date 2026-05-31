from __future__ import annotations

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import Photo, Report
from app.schemas import PhotoResponse
from app.services.photo_storage import photo_storage

router = APIRouter()


@router.post("/{report_id}", response_model=PhotoResponse, status_code=status.HTTP_201_CREATED)
def upload_photo(report_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    report = db.get(Report, report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    stored = photo_storage.save(file)
    photo = Photo(
        report_id=report_id,
        filename=stored["filename"],
        filepath=stored["filepath"],
        thumbnail_path=stored["thumbnail_path"],
    )
    db.add(photo)
    db.commit()
    db.refresh(photo)
    return photo


@router.delete("/{photo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_photo(photo_id: int, db: Session = Depends(get_db)):
    photo = db.get(Photo, photo_id)
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")
    photo_storage.delete(photo.filepath)
    db.delete(photo)
    db.commit()
    return None
