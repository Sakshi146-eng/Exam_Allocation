from fastapi import APIRouter, HTTPException
from bson import ObjectId
from datetime import datetime

from config.database import get_db
from models.staff import StaffCreate, StaffUpdate

router = APIRouter()


def staff_doc_to_dict(doc):
    """Convert a MongoDB staff document to a JSON-serialisable dict."""
    doc["_id"] = str(doc["_id"])
    return doc


# ── GET /  —  List all staff ─────────────────────────────────
@router.get("/")
async def get_all_staff():
    db = get_db()
    cursor = db.staffs.find().sort("name", 1)
    staff = [staff_doc_to_dict(s) async for s in cursor]
    return {"success": True, "count": len(staff), "data": staff}


# ── GET /available  —  List available staff ──────────────────
@router.get("/available")
async def get_available_staff():
    db = get_db()
    cursor = db.staffs.find({"isAvailable": True}).sort("name", 1)
    staff = [staff_doc_to_dict(s) async for s in cursor]
    return {"success": True, "count": len(staff), "data": staff}


# ── GET /{id}  —  Get single staff member ────────────────────
@router.get("/{id}")
async def get_staff(id: str):
    db = get_db()
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    doc = await db.staffs.find_one({"_id": ObjectId(id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Staff not found")
    return {"success": True, "data": staff_doc_to_dict(doc)}


# ── POST /  —  Create staff member ───────────────────────────
@router.post("/", status_code=201)
async def create_staff(staff: StaffCreate):
    db = get_db()
    now = datetime.utcnow()
    doc = {**staff.model_dump(), "createdAt": now, "updatedAt": now}
    result = await db.staffs.insert_one(doc)
    doc["_id"] = str(result.inserted_id)
    return {"success": True, "data": doc}


# ── PUT /{id}  —  Update staff member ────────────────────────
@router.put("/{id}")
async def update_staff(id: str, staff: StaffUpdate):
    db = get_db()
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    update_data = {k: v for k, v in staff.model_dump().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    update_data["updatedAt"] = datetime.utcnow()
    result = await db.staffs.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": update_data},
        return_document=True,
    )
    if not result:
        raise HTTPException(status_code=404, detail="Staff not found")
    return {"success": True, "data": staff_doc_to_dict(result)}


# ── DELETE /{id}  —  Delete staff member ─────────────────────
@router.delete("/{id}")
async def delete_staff(id: str):
    db = get_db()
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    result = await db.staffs.find_one_and_delete({"_id": ObjectId(id)})
    if not result:
        raise HTTPException(status_code=404, detail="Staff not found")
    return {"success": True, "data": {}}
