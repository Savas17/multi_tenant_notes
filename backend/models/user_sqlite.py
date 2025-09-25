from sqlalchemy import Column, Integer, String
from core.database_sqlite import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, default="user")
    tenant_id = Column(String, index=True)
    name = Column(String, default="")
    plan = Column(String, default="free")
