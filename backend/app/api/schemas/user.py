from pydantic import BaseModel, EmailStr
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from uuid import UUID

class UserBase(BaseModel):
    username: str
    email: str
    is_active: bool

# Sign up model
class UserCreate(UserBase):
    username:str
    email: EmailStr
    password: str
    repeat_password: str


# Model for login 
class UserLogin(BaseModel):
    email: str
    password: str

# Output model, the one that gets returned to the client
class UserResponse(UserBase):
    id: UUID
    class Config:
        from_attributes = True 

# User model used for writing into the database
class UserInDb(UserBase):
    id: UUID
    hashed_password: str


