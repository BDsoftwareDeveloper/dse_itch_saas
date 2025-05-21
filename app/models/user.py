# app/models/user.py

# from sqlalchemy.sql import func
# from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
# from sqlalchemy.orm import relationship
# from app.core.database import Base

# class User(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True, index=True)
#     email = Column(String, unique=True, index=True, nullable=False)
#     hashed_password = Column(String, nullable=False)
#     full_name = Column(String, nullable=True)
#     is_active = Column(Boolean, default=True)
#     is_superuser = Column(Boolean, default=False)
#     created_at = Column(DateTime, server_default=func.now())  # Database-side default
#     updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())  # Auto-update on change
#     tenant_id = Column(Integer, ForeignKey("tenants.id"))
#     tenant = relationship("Tenant", back_populates="users")


from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    role = Column(String, nullable=True)  # Add this line
    tenant_id = Column(Integer, ForeignKey("tenants.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    tenant = relationship("Tenant", back_populates="users")

