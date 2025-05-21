# # app/routers/user.py

# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.orm import Session
# from typing import List

# from app.schemas.user import UserOut, UserCreate
# from app.crud import user as crud_user
# from app.core.database import get_db
# from app.core.security import get_current_active_superuser

# router = APIRouter(
#     prefix="/users",
#     tags=["Users"],
#     dependencies=[Depends(get_current_active_superuser)],  # Superuser-only route
# )


# @router.post("/", response_model=UserOut)
# def create_user(user: UserCreate, db: Session = Depends(get_db)):
#     db_user = crud_user.get_user_by_email(db, user.email)
#     if db_user:
#         raise HTTPException(status_code=400, detail="Email already registered")
#     return crud_user.create_user(db, user)


# @router.get("/", response_model=List[UserOut])
# def list_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     return crud_user.get_users(db, skip=skip, limit=limit)


# @router.get("/{user_id}", response_model=UserOut)
# def get_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = crud_user.get_user(db, user_id)
#     if not db_user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user



# app/api/routers/user.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from app.db.base_class import get_db
from app.dependencies.auth import get_current_user
from app.schemas.user_schema import UserCreateSchema,UserOutSchema
from app.models.user import User
from app.utils.auth import hash_password

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserOutSchema)
def create_user(user: UserCreateSchema, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user_dict = user.model_dump()
    user_dict["hashed_password"] = hash_password(user.password)
    del user_dict["password"]
    new_user = User(**user_dict)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/me", dependencies=[Depends(get_current_user)])
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user