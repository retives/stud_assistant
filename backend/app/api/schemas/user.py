from pydantic import BaseModel, EmailStr
from uuid import UUID
# Input model
class UserCreate(BaseModel):
    username:str
    email: EmailStr
    password: str
    repeat_password: str

# Output model
class UserResponse(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    class Config:
        orm_mode = True