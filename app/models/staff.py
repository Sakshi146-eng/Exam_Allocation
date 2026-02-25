from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class StaffCreate(BaseModel):
    name: str = Field(..., min_length=1, description="Staff name")
    department: str = Field(..., min_length=1, description="Department")
    designation: str = Field(..., min_length=1, description="Designation")
    isAvailable: bool = Field(default=True, description="Whether staff is available for duty")


class StaffUpdate(BaseModel):
    name: Optional[str] = None
    department: Optional[str] = None
    designation: Optional[str] = None
    isAvailable: Optional[bool] = None


class StaffResponse(BaseModel):
    id: str = Field(..., alias="_id")
    name: str
    department: str
    designation: str
    isAvailable: bool
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None

    model_config = {"populate_by_name": True}
