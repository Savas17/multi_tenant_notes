from datetime import datetime
from typing import List
from data.fake_db import tenants

notes_db = []  # simple list to store notes

def get_notes_for_tenant(tenant_id: str) -> List[dict]:
    return [n for n in notes_db if n["tenantId"] == tenant_id]

def add_note(tenant_id: str, title: str, body: str, user):
    note_id = len(notes_db) + 1
    new_note = {
        "id": note_id,
        "title": title,
        "body": body,
        "tenantId": tenant_id,
        "createdAt": datetime.utcnow(),
        "createdBy": user["username"],
        "createdByName": user["name"],
    }
    notes_db.append(new_note)
    return new_note

def update_note(note_id: int, title: str, body: str, user):
    for note in notes_db:
        if note["id"] == note_id:
            if user["role"] != "admin" and note["createdBy"] != user["username"]:
                return None  # not authorized
            note["title"] = title
            note["body"] = body
            return note
    return None

def delete_note(note_id: int, user):
    global notes_db
    for note in notes_db:
        if note["id"] == note_id:
            if user["role"] != "admin" and note["createdBy"] != user["username"]:
                return False
            notes_db = [n for n in notes_db if n["id"] != note_id]
            return True
    return False
