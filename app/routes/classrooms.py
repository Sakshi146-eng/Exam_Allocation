from fastapi import APIRouter, HTTPException
from bson import ObjectId
from datetime import datetime

from config.database import get_db
from models.classroom import ClassroomCreate, ClassroomUpdate

router = APIRouter()


def classroom_doc_to_dict(doc):
    """Convert a MongoDB classroom document to a JSON-serialisable dict."""
    doc["_id"] = str(doc["_id"])
    return doc


# ── GET /  —  List all classrooms ────────────────────────────
@router.get("/")
async def get_all_classrooms():
    db = get_db()
    cursor = db.classrooms.find().sort([("block", 1), ("roomNumber", 1)])
    classrooms = [classroom_doc_to_dict(c) async for c in cursor]
    return {"success": True, "count": len(classrooms), "data": classrooms}


# ── GET /{id}  —  Get single classroom ──────────────────────
@router.get("/{id}")
async def get_classroom(id: str):
    db = get_db()
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    doc = await db.classrooms.find_one({"_id": ObjectId(id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Classroom not found")
    return {"success": True, "data": classroom_doc_to_dict(doc)}


# ── POST /  —  Create classroom ─────────────────────────────
@router.post("/", status_code=201)
async def create_classroom(classroom: ClassroomCreate):
    db = get_db()
    now = datetime.utcnow()
    doc = {**classroom.model_dump(), "createdAt": now, "updatedAt": now}
    try:
        result = await db.classrooms.insert_one(doc)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    doc["_id"] = str(result.inserted_id)
    return {"success": True, "data": doc}


# ── PUT /{id}  —  Update classroom ──────────────────────────
@router.put("/{id}")
async def update_classroom(id: str, classroom: ClassroomUpdate):
    db = get_db()
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    update_data = {k: v for k, v in classroom.model_dump().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    update_data["updatedAt"] = datetime.utcnow()
    result = await db.classrooms.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": update_data},
        return_document=True,
    )
    if not result:
        raise HTTPException(status_code=404, detail="Classroom not found")
    return {"success": True, "data": classroom_doc_to_dict(result)}


# ── DELETE /{id}  —  Delete classroom ────────────────────────
@router.delete("/{id}")
async def delete_classroom(id: str):
    db = get_db()
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    result = await db.classrooms.find_one_and_delete({"_id": ObjectId(id)})
    if not result:
        raise HTTPException(status_code=404, detail="Classroom not found")
    return {"success": True, "data": {}}
