from fastapi import APIRouter, HTTPException
from bson import ObjectId
from datetime import datetime

from config.database import get_db
from models.exam import ExamCreate, ExamUpdate

router = APIRouter()


def exam_doc_to_dict(doc):
    """Convert a MongoDB exam document to a JSON-serialisable dict."""
    doc["_id"] = str(doc["_id"])
    return doc


# ── GET /  —  List all exams ─────────────────────────────────
@router.get("/")
async def get_all_exams():
    db = get_db()
    cursor = db.ciaexams.find().sort("date", -1)
    exams = [exam_doc_to_dict(e) async for e in cursor]
    return {"success": True, "count": len(exams), "data": exams}


# ── GET /{id}  —  Get single exam ────────────────────────────
@router.get("/{id}")
async def get_exam(id: str):
    db = get_db()
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    doc = await db.ciaexams.find_one({"_id": ObjectId(id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Exam not found")
    return {"success": True, "data": exam_doc_to_dict(doc)}


# ── POST /  —  Create exam ──────────────────────────────────
@router.post("/", status_code=201)
async def create_exam(exam: ExamCreate):
    db = get_db()
    now = datetime.utcnow()
    doc = {**exam.model_dump(), "createdAt": now, "updatedAt": now}
    result = await db.ciaexams.insert_one(doc)
    doc["_id"] = str(result.inserted_id)
    return {"success": True, "data": doc}


# ── PUT /{id}  —  Update exam ───────────────────────────────
@router.put("/{id}")
async def update_exam(id: str, exam: ExamUpdate):
    db = get_db()
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    update_data = {k: v for k, v in exam.model_dump().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    update_data["updatedAt"] = datetime.utcnow()
    result = await db.ciaexams.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": update_data},
        return_document=True,
    )
    if not result:
        raise HTTPException(status_code=404, detail="Exam not found")
    return {"success": True, "data": exam_doc_to_dict(result)}


# ── DELETE /{id}  —  Delete exam ─────────────────────────────
@router.delete("/{id}")
async def delete_exam(id: str):
    db = get_db()
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    result = await db.ciaexams.find_one_and_delete({"_id": ObjectId(id)})
    if not result:
        raise HTTPException(status_code=404, detail="Exam not found")
    return {"success": True, "data": {}}
