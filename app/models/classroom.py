from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ClassroomCreate(BaseModel):
    roomNumber: str = Field(..., min_length=1, description="Room number")
    block: str = Field(..., min_length=1, description="Block")
    capacity: int = Field(..., ge=1, description="Seating capacity (minimum 1)")


class ClassroomUpdate(BaseModel):
    roomNumber: Optional[str] = None
    block: Optional[str] = None
    capacity: Optional[int] = Field(None, ge=1)


class ClassroomResponse(BaseModel):
    id: str = Field(..., alias="_id")
    roomNumber: str
    block: str
    capacity: int
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None

    model_config = {"populate_by_name": True}
