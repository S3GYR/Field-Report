from __future__ import annotations

from datetime import date, datetime
from enum import Enum
from typing import List, Optional

from sqlalchemy import Date, DateTime, Float, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class ReportStatus(str, Enum):
    draft = "draft"
    in_review = "in_review"
    approved = "approved"
    archived = "archived"


class WeatherType(str, Enum):
    sunny = "sunny"
    cloudy = "cloudy"
    rain = "rain"
    storm = "storm"
    snow = "snow"
    fog = "fog"
    unknown = "unknown"


class PhotoPriority(str, Enum):
    high = "high"
    medium = "medium"
    low = "low"
    none = "none"


class Report(Base):
    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    number: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    visit_date: Mapped[date] = mapped_column(Date, nullable=False)
    client: Mapped[str] = mapped_column(String(120), nullable=False)
    site: Mapped[str] = mapped_column(String(240), nullable=False)
    weather: Mapped[WeatherType] = mapped_column(SAEnum(WeatherType), default=WeatherType.unknown)
    comments: Mapped[Optional[str]] = mapped_column(Text)
    status: Mapped[ReportStatus] = mapped_column(
        SAEnum(ReportStatus), default=ReportStatus.draft, index=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    photos: Mapped[List["Photo"]] = relationship(
        back_populates="report", cascade="all, delete-orphan"
    )
    tasks: Mapped[List["Task"]] = relationship(
        back_populates="report", cascade="all, delete-orphan"
    )
    signature: Mapped[Optional["Signature"]] = relationship(
        back_populates="report", uselist=False, cascade="all, delete-orphan"
    )


class Photo(Base):
    __tablename__ = "photos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    report_id: Mapped[int] = mapped_column(ForeignKey("reports.id", ondelete="CASCADE"), index=True)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    filepath: Mapped[str] = mapped_column(String(500), nullable=False)
    thumbnail_path: Mapped[Optional[str]] = mapped_column(String(500))
    gps_lat: Mapped[Optional[float]] = mapped_column(Float)
    gps_lng: Mapped[Optional[float]] = mapped_column(Float)
    gps_accuracy: Mapped[Optional[float]] = mapped_column(Float)
    comment: Mapped[Optional[str]] = mapped_column(Text)
    priority: Mapped[PhotoPriority] = mapped_column(
        SAEnum(PhotoPriority), default=PhotoPriority.none
    )

    report: Mapped[Report] = relationship(back_populates="photos")
    tasks: Mapped[List["Task"]] = relationship(back_populates="photo", cascade="all, delete-orphan")


class TaskStatus(str, Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"
    blocked = "blocked"


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    report_id: Mapped[int] = mapped_column(ForeignKey("reports.id", ondelete="CASCADE"), index=True)
    photo_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("photos.id", ondelete="SET NULL"), index=True
    )
    description: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[TaskStatus] = mapped_column(
        SAEnum(TaskStatus), default=TaskStatus.todo, index=True
    )
    estimated_cost: Mapped[Optional[float]] = mapped_column(Numeric(12, 2))
    estimated_duration: Mapped[Optional[float]] = mapped_column(Float)

    report: Mapped[Report] = relationship(back_populates="tasks")
    photo: Mapped[Optional[Photo]] = relationship(back_populates="tasks")


class Signature(Base):
    __tablename__ = "signatures"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    report_id: Mapped[int] = mapped_column(
        ForeignKey("reports.id", ondelete="CASCADE"), unique=True
    )
    name: Mapped[str] = mapped_column(String(120))
    role: Mapped[Optional[str]] = mapped_column(String(120))
    signed_on: Mapped[Optional[date]] = mapped_column(Date)
    signature_image: Mapped[Optional[str]] = mapped_column(String(500))

    report: Mapped[Report] = relationship(back_populates="signature")
