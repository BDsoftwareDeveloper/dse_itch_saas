# app/dependencies/auth.py

from fastapi import Depends, HTTPException,Security
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from app.models.user import User
from app.db.base_class import get_db

oauth2_scheme =OAuth2PasswordBearer(tokenUrl="/auth/login") #OAuth2PasswordBearer(tokenUrl="/login")

# def get_current_user(token: str = Depends(oauth2_scheme), db=Depends(get_db)) -> User:
#     try:
#         payload = jwt.decode(token, "supersecret", algorithms=["HS256"])
#         user_id = payload.get("user_id")
#         tenant_id = payload.get("tenant_id")
#         if user_id is None:
#             raise HTTPException(status_code=401, detail="Invalid token")
#         user = db.query(User).filter(User.id == user_id, User.tenant_id == tenant_id).first()
#         if not user:
#             raise HTTPException(status_code=401, detail="User not found")
#         return user
#     except JWTError:
#         raise HTTPException(status_code=401, detail="Could not validate credentials")


def get_current_user(
    token: str = Security(oauth2_scheme),
    db=Depends(get_db)
) -> User:
    try:
        payload = jwt.decode(token, "supersecret", algorithms=["HS256"])
        user_id = payload.get("user_id")
        tenant_id = payload.get("tenant_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = db.query(User).filter(User.id == user_id, User.tenant_id == tenant_id).first()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

def require_role(role: str):
    def role_checker(user: User = Depends(get_current_user)):
        if user.role != role:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return user
    return role_checker
