from fastapi import APIRouter, Depends, HTTPException
from services.auth_service import get_current_user, require_admin
from core.database import tenants_collection

router = APIRouter()

# ✅ Get profile of logged-in user + tenant plan
@router.get("/me")
async def get_profile(user=Depends(get_current_user)):

    # Normalize tenant_id field (support both tenant_id and tenantId)
    tenant_id = user.get("tenant_id") or user.get("tenantId")
    tenant = await tenants_collection.find_one({"id": tenant_id})
    plan = tenant["plan"] if tenant else "free"

    return {
        "username": user["username"],
        "role": user["role"],
        "tenant_id": tenant_id,
        "plan": plan
    }

# ✅ Upgrade tenant plan (admin only)
@router.post("/upgrade")
async def upgrade_plan(user=Depends(require_admin)):

    tenant_id = user.get("tenant_id") or user.get("tenantId")

    result = await tenants_collection.update_one(
        {"id": tenant_id},
        {"$set": {"plan": "pro"}}
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=400, detail="Tenant not found")

    return {"message": f"Tenant {tenant_id} upgraded to Pro"}
