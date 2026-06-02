from __future__ import annotations

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import Photo, Report
from app.schemas import PhotoResponse, UpdatePhoto
from app.services.photo_storage import photo_storage

router = APIRouter()


@router.post("/{report_id}", response_model=PhotoResponse, status_code=status.HTTP_201_CREATED)
def upload_photo(
    report_id: int,
    file: UploadFile = File(...),
    gps_lat: float | None = Form(default=None),
    gps_lng: float | None = Form(default=None),
    gps_accuracy: float | None = Form(default=None),
    db: Session = Depends(get_db),
):
    report = db.get(Report, report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    stored = photo_storage.save(file)
    photo = Photo(
        report_id=report_id,
        filename=stored["filename"],
        filepath=stored["filepath"],
        thumbnail_path=stored["thumbnail_path"],
        gps_lat=gps_lat,
        gps_lng=gps_lng,
        gps_accuracy=gps_accuracy,
    )
    db.add(photo)
    db.commit()
    db.refresh(photo)
    return photo


@router.get("/", response_model=list[PhotoResponse])
def list_photos(db: Session = Depends(get_db)):
    return db.query(Photo).all()


@router.get("/{photo_id}", response_model=PhotoResponse)
def get_photo(photo_id: int, db: Session = Depends(get_db)):
    photo = db.get(Photo, photo_id)
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")
    return photo


@router.put("/{photo_id}", response_model=PhotoResponse)
def update_photo(photo_id: int, payload: UpdatePhoto, db: Session = Depends(get_db)):
    photo = db.get(Photo, photo_id)
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        if key not in ("id", "filename", "filepath", "thumbnail_path"):
            setattr(photo, key, value)
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
