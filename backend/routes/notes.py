from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from bson import ObjectId
from core.deps import get_current_user
from core.database import notes_collection
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/notes", tags=["Notes"])


class NoteCreate(BaseModel):
    title: str
    content: str


@router.get("/")
async def get_notes(user=Depends(get_current_user)):
    logger.info(f"Get notes requested by {user['username']} (tenant: {user['tenant_id']})")
    tenant_id = user["tenant_id"]
    notes = []
    async for note in notes_collection.find({"tenant_id": tenant_id}):
        notes.append({
            "id": str(note["_id"]),
            "title": note.get("title", ""),
            "body": note.get("content", ""),
            "createdBy": note.get("owner", ""),
            "createdAt": note.get("createdAt", None),
            "updatedAt": note.get("updatedAt", None),
        })
    return notes


@router.post("/")
async def create_note(note: NoteCreate, user=Depends(get_current_user)):
    logger.info(f"Create note requested by {user['username']} (tenant: {user['tenant_id']})")
    tenant_id = user["tenant_id"]

    if user.get("plan", "free") == "free":
        count = await notes_collection.count_documents({"tenant_id": tenant_id})
        logger.info(f"Tenant {tenant_id} notes count: {count}")
        if count >= 3:
            logger.warning("Free plan limit reached for tenant %s", tenant_id)
            raise HTTPException(403, "Free plan limit reached (3 notes). Upgrade to Pro.")

    new_note = {
        "title": note.title,
        "content": note.content,
        "tenant_id": tenant_id,
        "owner": user["username"],
        "createdAt": note.dict().get("createdAt"),
        "updatedAt": note.dict().get("updatedAt"),
    }
    result = await notes_collection.insert_one(new_note)
    logger.info(f"Note created with id {result.inserted_id}")

    return {
        "id": str(result.inserted_id),
        "message": "Note created"
    }


@router.put("/{note_id}")
async def update_note(note_id: str, note: NoteCreate, user=Depends(get_current_user)):
    logger.info(f"Update note {note_id} requested by {user['username']} (tenant: {user['tenant_id']})")
    tenant_id = user["tenant_id"]
    existing = await notes_collection.find_one({"_id": ObjectId(note_id), "tenant_id": tenant_id})
    if not existing:
        logger.warning(f"Note {note_id} not found")
        raise HTTPException(404, "Note not found")

    if user["role"] != "admin" and existing.get("owner") != user["username"]:
        logger.warning(f"User {user['username']} forbidden to edit note {note_id}")
        raise HTTPException(403, "Not allowed to edit this note")

    await notes_collection.update_one(
        {"_id": ObjectId(note_id)},
        {"$set": {"title": note.title, "content": note.content}}
    )
    logger.info(f"Note {note_id} updated")

    return {"id": note_id, "message": "Note updated"}


@router.delete("/{note_id}")
async def delete_note(note_id: str, user=Depends(get_current_user)):
    logger.info(f"Delete note {note_id} requested by {user['username']} (tenant: {user['tenant_id']})")
    tenant_id = user["tenant_id"]
    existing = await notes_collection.find_one({"_id": ObjectId(note_id), "tenant_id": tenant_id})
    if not existing:
        logger.warning(f"Note {note_id} not found for delete")
        raise HTTPException(404, "Note not found")

    if user["role"] != "admin" and existing.get("owner") != user["username"]:
        logger.warning(f"User {user['username']} forbidden to delete note {note_id}")
        raise HTTPException(403, "Not allowed to delete this note")

    await notes_collection.delete_one({"_id": ObjectId(note_id)})
    logger.info(f"Note {note_id} deleted")

    return {"id": note_id, "message": "Note deleted"}
