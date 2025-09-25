# from sqlalchemy import Column, Integer, String
# from sqlalchemy.orm import relationship
# from core.database import Base

# class Tenant(Base):
#     __tablename__ = "tenants"

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, unique=True, index=True)
#     plan = Column(String, default="free")

#     users = relationship("User", back_populates="tenants")
#     notes = relationship("Note", back_populates="tenants")
