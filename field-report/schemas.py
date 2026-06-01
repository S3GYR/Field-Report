from __future__ import annotations

from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, Field
from pydantic.config import ConfigDict

from models import PhotoPriority, ReportStatus, TaskStatus, WeatherType


class PhotoBase(BaseModel):
    comment: Optional[str] = None
    priority: PhotoPriority = PhotoPriority.none
    gps_lat: Optional[float] = Field(default=None, ge=-90, le=90)
    gps_lng: Optional[float] = Field(default=None, ge=-180, le=180)


class CreatePhoto(PhotoBase):
    filename: str


class UpdatePhoto(PhotoBase):
    comment: Optional[str] = None
    priority: Optional[PhotoPriority] = None
    gps_lat: Optional[float] = Field(default=None, ge=-90, le=90)
    gps_lng: Optional[float] = Field(default=None, ge=-180, le=180)


class PhotoResponse(PhotoBase):
    id: int
    filename: str
    filepath: str
    thumbnail_path: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class TaskBase(BaseModel):
    description: str
    status: TaskStatus = TaskStatus.todo
    estimated_cost: Optional[float] = Field(default=None, ge=0)
    estimated_duration: Optional[float] = Field(default=None, ge=0)


class CreateTask(TaskBase):
    photo_id: Optional[int] = None


class UpdateTask(BaseModel):
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    estimated_cost: Optional[float] = Field(default=None, ge=0)
    estimated_duration: Optional[float] = Field(default=None, ge=0)
    photo_id: Optional[int] = None


class TaskResponse(TaskBase):
    id: int
    photo_id: Optional[int]

    model_config = ConfigDict(from_attributes=True)


class SignatureBase(BaseModel):
    name: str
    role: Optional[str] = None
    signed_on: Optional[date] = None
    signature_image: Optional[str] = None


class CreateSignature(SignatureBase):
    pass


class UpdateSignature(BaseModel):
    name: Optional[str] = None
    role: Optional[str] = None
    signed_on: Optional[date] = None
    signature_image: Optional[str] = None


class SignatureResponse(SignatureBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class ReportBase(BaseModel):
    number: str
    visit_date: date
    client: str
    site: str
    weather: WeatherType = WeatherType.unknown
    comments: Optional[str] = None
    status: ReportStatus = ReportStatus.draft


class CreateReport(ReportBase):
    pass


class UpdateReport(BaseModel):
    number: Optional[str] = None
    visit_date: Optional[date] = None
    client: Optional[str] = None
    site: Optional[str] = None
    weather: Optional[WeatherType] = None
    comments: Optional[str] = None
    status: Optional[ReportStatus] = None


class ReportResponse(ReportBase):
    id: int
    created_at: datetime
    updated_at: datetime
    photos: List[PhotoResponse] = Field(default_factory=list)
    tasks: List[TaskResponse] = Field(default_factory=list)
    signature: Optional[SignatureResponse] = None

    model_config = ConfigDict(from_attributes=True)
