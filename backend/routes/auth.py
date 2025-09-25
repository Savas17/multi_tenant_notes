# routes/auth.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import timedelta
from services.auth_service import authenticate_user, create_access_token_with_exp

router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login")
async def login(request: LoginRequest):
    # 🔹 Authenticate user
    user = await authenticate_user(request.username, request.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # 🔹 Generate JWT
    access_token_expires = timedelta(minutes=60)
    access_token = create_access_token_with_exp(
        data={
            "sub": user["username"],
            "role": user["role"],
            "tenant_id": user["tenant_id"],
        },
        expires_delta=access_token_expires
    )

    # 🔹 Return token + user info including plan
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user["id"],
            "username": user["username"],
            "role": user["role"],
            "tenant_id": user["tenant_id"],
            "name": user.get("name", ""),
            "plan": user.get("plan", "free"),
        }
    }
