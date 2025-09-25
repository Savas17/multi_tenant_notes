# from sqlalchemy import Column, Integer, String, Text, ForeignKey
# from sqlalchemy.orm import relationship
# from core.database import Base

# class Note(Base):
#     __tablename__ = "notes"

#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, nullable=False)
#     body = Column(Text)
#     tenant_id = Column(Integer, ForeignKey("tenants.id"))
#     created_by = Column(Integer, ForeignKey("users.id"))

#     tenant = relationship("Tenant", back_populates="notes")
