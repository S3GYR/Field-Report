from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import Report, Signature
from app.schemas import CreateSignature, SignatureResponse, UpdateSignature

router = APIRouter()


@router.post("/{report_id}", response_model=SignatureResponse, status_code=status.HTTP_201_CREATED)
def create_signature(report_id: int, payload: CreateSignature, db: Session = Depends(get_db)):
    report = db.get(Report, report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    signature = Signature(report_id=report_id, **payload.model_dump())
    db.add(signature)
    db.commit()
    db.refresh(signature)
    return signature


@router.put("/{report_id}", response_model=SignatureResponse)
def update_signature(report_id: int, payload: UpdateSignature, db: Session = Depends(get_db)):
    signature = db.query(Signature).filter(Signature.report_id == report_id).one_or_none()
    if not signature:
        raise HTTPException(status_code=404, detail="Signature not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(signature, key, value)
    db.add(signature)
    db.commit()
    db.refresh(signature)
    return signature


@router.delete("/{report_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_signature(report_id: int, db: Session = Depends(get_db)):
    signature = db.query(Signature).filter(Signature.report_id == report_id).one_or_none()
    if not signature:
        raise HTTPException(status_code=404, detail="Signature not found")
    db.delete(signature)
    db.commit()
    return None
