from sqlalchemy import Column, Integer, String
from core.database_sqlite import Base

class Tenant(Base):
    __tablename__ = "tenants"
    id = Column(String, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    plan = Column(String, default="free")
