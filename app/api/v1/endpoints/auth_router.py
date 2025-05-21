# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.orm import Session
# from app.crud import user
# from app.core.database import get_db
# from app.core.security import create_access_token
# from app.schemas import auth

# router = APIRouter(
#     prefix="/v1/auth",
#     tags=["Authentication"]
# )

# @router.post("/login", response_model=auth.Token)
# def login(user_credentials: auth.UserLogin, db: Session = Depends(get_db)):
#     user = user.authenticate_user(db, user_credentials.username, user_credentials.password)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid Credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )

#     access_token = create_access_token(data={"sub": user.username})
#     return {"access_token": access_token, "token_type": "bearer"}



from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.token import Token
from app.db.base_class import get_db
from app.models.user import User
from app.models.tenant import Tenant
from app.schemas.user_schema import UserCreateSchema, UserOutSchema

from app.utils.security import verify_password, create_access_token
from datetime import timedelta
from app.utils.auth import hash_password

router = APIRouter(prefix="/auth", tags=["Auth"])



@router.post("/register", response_model=UserOutSchema)
def register_user(user_data: UserCreateSchema, db: Session = Depends(get_db)):
    tenant = db.query(Tenant).filter(Tenant.id == user_data.tenant_id).first()
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")

    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=409, detail="Email already registered")

    user = User(
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=hash_password(user_data.password),
        tenant_id=user_data.tenant_id,
        role=user_data.role  # e.g., 'admin', 'user'
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/login")
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token_data = {
        "sub": user.email,
        "user_id": user.id,
        "tenant_id": user.tenant_id,
        "role": user.role
    }

    access_token = create_access_token(data=token_data)
    return {"access_token": access_token, "token_type": "bearer"}
