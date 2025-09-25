from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import auth_sqlite, notes_sqlite, tenants_sqlite, users_sqlite  # add users_sqlite here
import os
from dotenv import load_dotenv


load_dotenv()


app = FastAPI(
    title="Multi-Tenant Notes App",
    description="Notes app with tenant isolation, roles, and subscription plans",
    version="1.0.0"
)


# Allow multiple frontend URLs from .env or default values for dev
origins = os.getenv("FRONTEND_URL", "http://localhost:5173").split(",")



app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow frontend origins for CORS
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "ok"}


# Register routers with appropriate prefixes and tags
app.include_router(auth_sqlite.router, prefix="/auth", tags=["Auth"])
app.include_router(notes_sqlite.router, prefix="/notes", tags=["Notes"])
app.include_router(tenants_sqlite.router, prefix="/tenants", tags=["Tenants"])
app.include_router(users_sqlite.router, prefix="/users", tags=["Users"]) 
