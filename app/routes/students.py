from fastapi import APIRouter, HTTPException, Query
from bson import ObjectId
from datetime import datetime
from typing import Optional, List

from config.database import get_db
from models.student import StudentCreate, StudentUpdate

router = APIRouter()


def student_doc_to_dict(doc):
    """Convert a MongoDB student document to a JSON-serialisable dict."""
    doc["_id"] = str(doc["_id"])
    return doc


# ── GET /  —  List students (optional semester/department filter) ─
@router.get("/")
async def get_all_students(
    semester: Optional[int] = Query(None, ge=1, le=8),
    department: Optional[str] = Query(None),
):
    db = get_db()
    filter_query = {}
    if semester is not None:
        filter_query["semester"] = semester
    if department is not None:
        filter_query["department"] = department

    cursor = db.students.find(filter_query).sort(
        [("semester", 1), ("department", 1), ("usn", 1)]
    )
    students = [student_doc_to_dict(s) async for s in cursor]
    return {"success": True, "count": len(students), "data": students}


# ── GET /usn/{usn}  —  Get student by USN ────────────────────
@router.get("/usn/{usn}")
async def get_student_by_usn(usn: str):
    db = get_db()
    doc = await db.students.find_one({"usn": usn.upper()})
    if not doc:
        raise HTTPException(status_code=404, detail="Student not found with this USN")
    return {"success": True, "data": student_doc_to_dict(doc)}


# ── GET /{id}  —  Get single student ─────────────────────────
@router.get("/{id}")
async def get_student(id: str):
    db = get_db()
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    doc = await db.students.find_one({"_id": ObjectId(id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"success": True, "data": student_doc_to_dict(doc)}


# ── POST /  —  Create student ────────────────────────────────
@router.post("/", status_code=201)
async def create_student(student: StudentCreate):
    db = get_db()
    now = datetime.utcnow()
    doc = {**student.model_dump(), "createdAt": now, "updatedAt": now}
    try:
        result = await db.students.insert_one(doc)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    doc["_id"] = str(result.inserted_id)
    return {"success": True, "data": doc}


# ── POST /bulk  —  Bulk create students ──────────────────────
@router.post("/bulk", status_code=201)
async def bulk_create_students(students: List[StudentCreate]):
    db = get_db()
    if not students:
        raise HTTPException(status_code=400, detail="Provide an array of students")
    now = datetime.utcnow()
    docs = [{**s.model_dump(), "createdAt": now, "updatedAt": now} for s in students]
    try:
        result = await db.students.insert_many(docs, ordered=False)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    # Re-fetch the inserted docs to return them with _id
    inserted = []
    async for doc in db.students.find({"_id": {"$in": result.inserted_ids}}):
        inserted.append(student_doc_to_dict(doc))
    return {"success": True, "count": len(inserted), "data": inserted}


# ── PUT /{id}  —  Update student ─────────────────────────────
@router.put("/{id}")
async def update_student(id: str, student: StudentUpdate):
    db = get_db()
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    update_data = {k: v for k, v in student.model_dump().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    update_data["updatedAt"] = datetime.utcnow()
    result = await db.students.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": update_data},
        return_document=True,
    )
    if not result:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"success": True, "data": student_doc_to_dict(result)}


# ── DELETE /{id}  —  Delete student ──────────────────────────
@router.delete("/{id}")
async def delete_student(id: str):
    db = get_db()
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    result = await db.students.find_one_and_delete({"_id": ObjectId(id)})
    if not result:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"success": True, "data": {}}
