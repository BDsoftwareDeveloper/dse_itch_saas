# app/routers/tenant.py
# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from app.schemas.tenant import TenantCreate, TenantOut
# from app.crud.tenant import create_tenant
# from app.core.database import get_db

# router = APIRouter(prefix="/tenants", tags=["Tenants"])

# @router.post("/", response_model=TenantOut)
# def create(tenant: TenantCreate, db: Session = Depends(get_db)):
#     return create_tenant(db, tenant)



from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from app.db.base_class import get_db
from app.schemas.tenant import TenantCreate,TenantResponse
from app.models.tenant import Tenant

router = APIRouter(prefix="/tenants", tags=["Tenants"])

@router.post("/", response_model=TenantResponse)
def create_tenant(tenant: TenantCreate, db: Session = Depends(get_db)):
    db_tenant = db.query(Tenant).filter(Tenant.name == tenant.name).first()
    if db_tenant:
        raise HTTPException(status_code=400, detail="Tenant already exists")
    new_tenant = Tenant(**tenant.model_dump())
    db.add(new_tenant)
    db.commit()
    db.refresh(new_tenant)
    return new_tenant

@router.get("/{tenant_id}", response_model=TenantResponse)
def get_tenant(tenant_id: UUID, db: Session = Depends(get_db)):
    tenant = db.query(Tenant).get(tenant_id)
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return tenant