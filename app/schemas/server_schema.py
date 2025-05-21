

from pydantic import BaseModel
from typing import Optional

from app.crud import tenant

class ServerCreateSchema(BaseModel):
    name: str
    primary_ip: str
    failover_ip: str
    port: int
    username: str
    password: str
    description: Optional[str] = None
    tenant_id: int
    

class ServerUpdateSchema(BaseModel):
    name: Optional[str] = None
    primary_ip: Optional[str] = None
    failover_ip: Optional[str] = None
    port: Optional[int] = None
    username: Optional[str] = None
    password: Optional[str] = None
    description: Optional[str] = None
    tenant_id: Optional[int] = None  # ✅ fixed type
   

class ServerOutSchema(ServerCreateSchema):
    id: int
    name: str
    primary_ip: str
    failover_ip: str
    port: int
    username: str
    password: str
    description: str
    tenant_id: int
    class Config:
        from_attributes = True

