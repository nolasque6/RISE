from pydantic import BaseModel, EmailStr

class UserResponse(BaseModel):
    id: int
    full_name: str
    email: str

class UserUpdate(BaseModel):
    full_name: str | None = None
    email: EmailStr | None = None

class UserRegister(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"