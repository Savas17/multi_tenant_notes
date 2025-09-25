from core.database import tenants_collection

async def get_tenant_by_id(tenant_id: str):
    return await tenants_collection.find_one({"id": tenant_id})

async def upgrade_tenant_plan(tenant_id: str, new_plan: str = "pro"):
    result = await tenants_collection.update_one(
        {"id": tenant_id}, {"$set": {"plan": new_plan}}
    )
    return result.modified_count > 0
