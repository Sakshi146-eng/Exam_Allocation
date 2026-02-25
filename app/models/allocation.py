from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class RoomAllocationResponse(BaseModel):
    room: str
    roomNumber: str
    block: str
    capacity: int
    staffAssigned: List[str] = []
    studentsAssigned: List[str] = []


class AllocationResponse(BaseModel):
    id: str = Field(..., alias="_id")
    examId: str
    roomAllocations: List[RoomAllocationResponse] = []
    totalStudentsAllocated: int = 0
    totalRoomsUsed: int = 0
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None

    model_config = {"populate_by_name": True}
