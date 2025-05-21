# # app/schemas/auth.py

# from pydantic import BaseModel, EmailStr
# from typing import Optional


# # app/schemas/auth.py

# from pydantic import BaseModel, EmailStr
# from typing import Optional


# class Token(BaseModel):
#     access_token: str
#     token_type: str = "bearer"


# class TokenData(BaseModel):
#     username: Optional[str] = None


# # Renaming LoginRequest to UserLogin
# class UserLogin(BaseModel):
#     email: EmailStr
#     password: str


# class SignupRequest(BaseModel):
#     email: EmailStr
#     password: str
#     full_name: Optional[str] = None


# class UserResponse(BaseModel):
#     id: int
#     email: EmailStr
#     is_active: bool
#     is_superuser: bool

#     class Config:
#         orm_mode = True




from pydantic import BaseModel

class LoginRequest(BaseModel):
    email: str
    password: str
