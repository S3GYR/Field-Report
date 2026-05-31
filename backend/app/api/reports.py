from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import Photo, Report, Signature, Task
from app.schemas import CreateReport, ReportResponse, UpdateReport
from app.services.pdf_service import report_pdf_service

router = APIRouter()


@router.get("/", response_model=List[ReportResponse])
def list_reports(db: Session = Depends(get_db)):
    return db.query(Report).all()


@router.post("/", response_model=ReportResponse, status_code=status.HTTP_201_CREATED)
def create_report(payload: CreateReport, db: Session = Depends(get_db)):
    report = Report(**payload.model_dump())
    db.add(report)
    db.commit()
    db.refresh(report)
    return report


@router.get("/{report_id}", response_model=ReportResponse)
def get_report(report_id: int, db: Session = Depends(get_db)):
    report = db.get(Report, report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report


@router.put("/{report_id}", response_model=ReportResponse)
def update_report(report_id: int, payload: UpdateReport, db: Session = Depends(get_db)):
    report = db.get(Report, report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(report, key, value)
    db.add(report)
    db.commit()
    db.refresh(report)
    return report


@router.delete("/{report_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_report(report_id: int, db: Session = Depends(get_db)):
    report = db.get(Report, report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    db.delete(report)
    db.commit()
    return None


@router.post("/{report_id}/generate-pdf", status_code=status.HTTP_201_CREATED)
def generate_report_pdf(report_id: int, db: Session = Depends(get_db)):
    report = db.get(Report, report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    try:
        pdf_path = report_pdf_service.generate_pdf(report_id)
    except ValueError as exc:  # defensive: report removed between calls
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {"pdf": str(pdf_path)}
