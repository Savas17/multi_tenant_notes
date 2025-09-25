from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from core.security import decode_access_token
from core.database import users_collection

# Token URL = /auth/login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# ✅ Get logged-in user from JWT
async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    username: str = payload.get("sub")
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload (missing sub)",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await users_collection.find_one({"username": username})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    # Normalize user object
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "role": user["role"],
        "tenant_id": user["tenantId"],  # 👈 match your seeded DB
        "name": user.get("name", ""),
        "plan": user.get("plan", "free")
    }

# ✅ Require admin role
async def require_admin(user: dict = Depends(get_current_user)):
    if user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return user

# ✅ Require member role
async def require_member(user: dict = Depends(get_current_user)):
    if user["role"] != "member":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Member access required"
        )
    return user
