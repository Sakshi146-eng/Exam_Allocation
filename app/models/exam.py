from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ExamCreate(BaseModel):
    examName: str = Field(..., min_length=1, description="Exam name")
    date: datetime = Field(..., description="Exam date")
    semester: int = Field(..., ge=1, le=8, description="Target semester (1-8)")


class ExamUpdate(BaseModel):
    examName: Optional[str] = None
    date: Optional[datetime] = None
    semester: Optional[int] = Field(None, ge=1, le=8)


class ExamResponse(BaseModel):
    id: str = Field(..., alias="_id")
    examName: str
    date: datetime
    semester: int
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None

    model_config = {"populate_by_name": True}
