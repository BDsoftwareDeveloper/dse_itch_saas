# app/schemas/tenant.py
# from pydantic import BaseModel,ConfigDict
# from datetime import datetime

# class TenantCreate(BaseModel):
#     name: str
#     schema_name: str

# class TenantOut(BaseModel):
#     id: int
#     name: str
#     schema_name: str
#     created_at: datetime

#     class Config:
#         from_attributes = True


from pydantic import BaseModel
from datetime import datetime

class TenantBase(BaseModel):
    name: str

class TenantCreate(TenantBase):
    pass

class TenantResponse(TenantBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
