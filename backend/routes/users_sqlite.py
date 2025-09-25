from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from models.user_sqlite import User
from core.database_sqlite import SessionLocal
from core.deps_sqlite import get_current_user

router = APIRouter()

class UserInvite(BaseModel):
    email: str
    role: str  # e.g. "member" or "admin"
    tenant_id: str

class PlanChangeRequest(BaseModel):
    new_plan: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/invite")
async def invite_user(invite: UserInvite, user=Depends(get_current_user), db: Session = Depends(get_db)):
    if user.role != "admin":
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Only Admins can invite users")

    existing_user = db.query(User).filter(User.email == invite.email).first()
    if existing_user:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "User with this email already exists")

    new_user = User(
        username=invite.email,
        password="defaultpassword",  # Please hash in real app
        role=invite.role,
        tenant_id=invite.tenant_id,
        name="",
        plan="free"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": f"User invited successfully with email {invite.email}"}

@router.get("/count-members")
async def count_members(user=Depends(get_current_user), db: Session=Depends(get_db)):
    if user.role != "admin":
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Only admins can view member count")
    count = db.query(User).filter(User.tenant_id == user.tenant_id, User.role == "member").count()
    return {"member_count": count}

@router.get("/list-members")
async def list_members(user=Depends(get_current_user), db: Session = Depends(get_db)):
    if user.role != "admin":
        raise HTTPException(403, "Only admin can list members")
    members = db.query(User).filter(User.tenant_id == user.tenant_id, User.role == "member").all()
    return [
        {"id": member.id, "username": member.username, "name": member.name, "plan": member.plan}
        for member in members
    ]

@router.post("/change-plan/{user_id}")
async def change_member_plan(
    user_id: int,
    request: PlanChangeRequest,
    user=Depends(get_current_user),
    db: Session=Depends(get_db)
):
    new_plan = request.new_plan
    if user.role != "admin":
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Only admins can change member plans")

    member = db.query(User).filter(User.id == user_id).first()
    if not member:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Member not found")
    if member.role != "member":
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Can only change plan for members")
    if new_plan not in ["free", "pro"]:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid plan")

    member.plan = new_plan
    db.commit()
    return {"message": f"Plan changed to {new_plan} for user {member.username}"}
