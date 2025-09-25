from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from core.database_sqlite import SessionLocal
from models.tenant_sqlite import Tenant
from core.deps_sqlite import get_current_user

router = APIRouter()

class TenantCreate(BaseModel):
    name: str
    plan: str = "free"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
async def get_tenants(db: Session = Depends(get_db)):
    tenants = db.query(Tenant).all()
    return [
        {
            "id": tenant.id,
            "name": tenant.name,
            "plan": tenant.plan
        }
        for tenant in tenants
    ]

@router.post("/")
async def create_tenant(tenant: TenantCreate, db: Session = Depends(get_db)):
    db_tenant = Tenant(**tenant.dict())
    db.add(db_tenant)
    db.commit()
    db.refresh(db_tenant)
    return {"id": db_tenant.id}

@router.post("/upgrade")
async def upgrade_plan(user=Depends(get_current_user), db: Session = Depends(get_db)):
    if user.role != "admin":
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Only admin can upgrade tenant plan")
    tenant = db.query(Tenant).filter(Tenant.id == user.tenant_id).first()
    if not tenant:
        raise HTTPException(404, "Tenant not found")
    if tenant.plan == "pro":
        return {"plan": "pro", "message": "Tenant is already on Pro plan"}
    tenant.plan = "pro"
    db.commit()
    return {"plan": "pro", "message": "Tenant upgraded to Pro plan successfully"}
