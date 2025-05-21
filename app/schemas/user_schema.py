
# app/schemas/user_schema.py

from pydantic import BaseModel, EmailStr

class UserCreateSchema(BaseModel):
    email: EmailStr
    full_name: str
    password: str
    tenant_id: int
    role: str  # e.g., 'admin' or 'user'

class UserOutSchema(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role: str
    tenant_id: int

    class Config:
        from_attributes = True

