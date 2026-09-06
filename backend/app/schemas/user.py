from pydantic import BaseModel, EmailStr

class UserResponse(BaseModel):
    id: int
    full_name: str
    email: str

class UserUpdate(BaseModel):
    full_name: str | None = None
    email: EmailStr | None = None