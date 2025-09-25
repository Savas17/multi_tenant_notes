from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from core.database import users_collection

SECRET_KEY = "supersecret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# --- Authenticate user ---
async def authenticate_user(username: str, password: str):
    user = await users_collection.find_one({"username": username, "password": password})
    if not user:
        return None
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "role": user["role"],
        "tenant_id": user.get("tenant_id") or user.get("tenantId"),  # normalize
        "name": user.get("name", ""),
        "plan": user.get("plan", "free")
    }

# --- JWT create token ---
def create_access_token_with_exp(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# --- Dependency: get current user ---
async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

        user = await users_collection.find_one({"username": username})
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

        return {
            "id": str(user["_id"]),
            "username": user["username"],
            "role": user["role"],
            "tenant_id": user.get("tenant_id") or user.get("tenantId"),
            "name": user.get("name", ""),
            "plan": user.get("plan", "free")
        }
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

# --- Dependency: require admin ---
async def require_admin(user=Depends(get_current_user)):
    if user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return user
