from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel
from sqlalchemy.orm import Session
from models.user_sqlite import User
from models.tenant_sqlite import Tenant
from models.note_sqlite import Note
from core.database_sqlite import SessionLocal
from core.deps_sqlite import get_current_user

router = APIRouter()

class NoteCreate(BaseModel):
    title: str
    content: str
    tenant_id: str
    owner: int

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
async def get_notes(tenant_id: str, db: Session = Depends(get_db)):
    notes = db.query(Note).filter_by(tenant_id=tenant_id).all()
    return [
        {
            "id": note.id,
            "title": note.title,
            "body": note.content,
            "owner": note.owner,
            "tenant_id": note.tenant_id,
            "createdAt": note.createdAt,
            "updatedAt": note.updatedAt,
            "createdBy": note.owner
        }
        for note in notes
    ]

@router.post("/")
async def create_note(note: NoteCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    tenant = db.query(Tenant).filter_by(id=user.tenant_id).first()
    if not tenant:
        raise HTTPException(404, "Tenant not found")

    # Only limit for members on free plan, admins have unlimited
    if tenant.plan == "free" and user.role != "admin":
        count = db.query(Note).filter_by(tenant_id=user.tenant_id).count()
        if count >= 3:
            raise HTTPException(403, "Free plan tenant note limit reached (3 notes).")

    db_note = Note(**note.dict())
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return {"id": db_note.id}

@router.put("/{note_id}")
async def update_note(note_id: int, note: NoteCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_note = db.query(Note).filter_by(id=note_id).first()
    if not db_note:
        raise HTTPException(404, "Note not found")

    # Allow all users to edit any note (remove ownership check)
    db_note.title = note.title
    db_note.content = note.content
    db_note.tenant_id = note.tenant_id
    db_note.owner = note.owner

    db.commit()
    db.refresh(db_note)
    return {"id": db_note.id}

@router.delete("/{note_id}")
async def delete_note(note_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_note = db.query(Note).filter_by(id=note_id).first()
    if not db_note:
        raise HTTPException(404, "Note not found")

    # Allow all users to delete any note
    db.delete(db_note)
    db.commit()
    return {"id": note_id}

@router.get("/{note_id}")
async def get_note(note_id: int = Path(..., description="The ID of the note to retrieve"),
                   user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_note = db.query(Note).filter_by(id=note_id).first()
    if not db_note:
        raise HTTPException(404, "Note not found")

    # Allow all users to view any note
    return {
        "id": db_note.id,
        "title": db_note.title,
        "body": db_note.content,
        "owner": db_note.owner,
        "tenant_id": db_note.tenant_id,
        "createdAt": db_note.createdAt,
        "updatedAt": db_note.updatedAt,
        "createdBy": db_note.owner
    }
