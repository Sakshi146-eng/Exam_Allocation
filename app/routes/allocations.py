from fastapi import APIRouter, HTTPException
from bson import ObjectId
from datetime import datetime

from config.database import get_db
from services.allocation_engine import generate_allocation

router = APIRouter()


def _stringify_ids(doc):
    """Recursively convert ObjectId values to strings in a document."""
    if isinstance(doc, dict):
        return {k: _stringify_ids(v) for k, v in doc.items()}
    elif isinstance(doc, list):
        return [_stringify_ids(item) for item in doc]
    elif isinstance(doc, ObjectId):
        return str(doc)
    return doc


# ── GET /  —  List all allocations ───────────────────────────
@router.get("/")
async def get_all_allocations():
    db = get_db()
    allocations = []
    async for alloc in db.allocations.find().sort("createdAt", -1):
        # Populate exam info
        if alloc.get("examId"):
            exam = await db.ciaexams.find_one({"_id": alloc["examId"]})
            if exam:
                alloc["examId"] = {
                    "_id": str(exam["_id"]),
                    "examName": exam.get("examName"),
                    "date": exam.get("date"),
                    "semester": exam.get("semester"),
                }
            else:
                alloc["examId"] = str(alloc["examId"])
        allocations.append(_stringify_ids(alloc))
    return {"success": True, "count": len(allocations), "data": allocations}


# ── POST /generate/{exam_id}  —  Generate allocation for exam
@router.post("/generate/{exam_id}", status_code=201)
async def generate_exam_allocation(exam_id: str):
    db = get_db()
    if not ObjectId.is_valid(exam_id):
        raise HTTPException(status_code=400, detail="Invalid exam ID format")

    exam = await db.ciaexams.find_one({"_id": ObjectId(exam_id)})
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")

    # Check if allocation already exists
    existing = await db.allocations.find_one({"examId": exam["_id"]})
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Allocation already exists for this exam. Delete it first to regenerate.",
        )

    # Run the allocation engine
    try:
        result = await generate_allocation(exam["semester"])
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Save to database
    now = datetime.utcnow()
    alloc_doc = {
        "examId": exam["_id"],
        "roomAllocations": result["roomAllocations"],
        "totalStudentsAllocated": result["totalStudentsAllocated"],
        "totalRoomsUsed": result["totalRoomsUsed"],
        "createdAt": now,
        "updatedAt": now,
    }
    insert_result = await db.allocations.insert_one(alloc_doc)
    alloc_doc["_id"] = insert_result.inserted_id

    return {
        "success": True,
        "data": _stringify_ids(alloc_doc),
        "summary": {
            "totalStudents": result["totalStudents"],
            "totalStudentsAllocated": result["totalStudentsAllocated"],
            "unallocatedCount": result["unallocatedCount"],
            "totalRoomsUsed": result["totalRoomsUsed"],
        },
    }


# ── GET /exam/{exam_id}  —  Get allocation by exam (populated)
@router.get("/exam/{exam_id}")
async def get_allocation_by_exam(exam_id: str):
    db = get_db()
    if not ObjectId.is_valid(exam_id):
        raise HTTPException(status_code=400, detail="Invalid exam ID format")

    alloc = await db.allocations.find_one({"examId": ObjectId(exam_id)})
    if not alloc:
        raise HTTPException(
            status_code=404, detail="No allocation found for this exam"
        )

    # Populate exam
    exam = await db.ciaexams.find_one({"_id": alloc["examId"]})
    if exam:
        alloc["examId"] = _stringify_ids(exam)

    # Populate room allocations
    for ra in alloc.get("roomAllocations", []):
        # Populate room
        if ra.get("room"):
            room = await db.classrooms.find_one({"_id": ra["room"]})
            if room:
                ra["room"] = _stringify_ids(room)

        # Populate staff
        populated_staff = []
        for staff_id in ra.get("staffAssigned", []):
            staff = await db.staffs.find_one({"_id": staff_id})
            if staff:
                populated_staff.append(
                    {
                        "_id": str(staff["_id"]),
                        "name": staff.get("name"),
                        "department": staff.get("department"),
                        "designation": staff.get("designation"),
                    }
                )
        ra["staffAssigned"] = populated_staff

        # Populate students
        populated_students = []
        for student_id in ra.get("studentsAssigned", []):
            student = await db.students.find_one({"_id": student_id})
            if student:
                populated_students.append(
                    {
                        "_id": str(student["_id"]),
                        "usn": student.get("usn"),
                        "name": student.get("name"),
                        "semester": student.get("semester"),
                        "department": student.get("department"),
                    }
                )
        ra["studentsAssigned"] = populated_students

    return {"success": True, "data": _stringify_ids(alloc)}


# ── DELETE /{id}  —  Delete allocation ───────────────────────
@router.delete("/{id}")
async def delete_allocation(id: str):
    db = get_db()
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    result = await db.allocations.find_one_and_delete({"_id": ObjectId(id)})
    if not result:
        raise HTTPException(status_code=404, detail="Allocation not found")
    return {"success": True, "data": {}}
