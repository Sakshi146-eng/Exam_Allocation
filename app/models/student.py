from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class StudentCreate(BaseModel):
    usn: str = Field(..., min_length=10, max_length=10, description="10-digit University Seat Number")
    name: str = Field(..., min_length=1, description="Student name")
    semester: int = Field(..., ge=1, le=8, description="Semester (1-8)")
    department: str = Field(..., min_length=1, description="Department")


class StudentUpdate(BaseModel):
    usn: Optional[str] = Field(None, min_length=10, max_length=10)
    name: Optional[str] = None
    semester: Optional[int] = Field(None, ge=1, le=8)
    department: Optional[str] = None


class StudentResponse(BaseModel):
    id: str = Field(..., alias="_id")
    usn: str
    name: str
    semester: int
    department: str
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None

    model_config = {"populate_by_name": True}
