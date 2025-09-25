from sqlalchemy import Column, Integer, String, Text, ForeignKey
from core.database_sqlite import Base

class Note(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    owner = Column(Integer, ForeignKey("users.id"))
    tenant_id = Column(String, index=True)
    createdAt = Column(String)
    updatedAt = Column(String)
