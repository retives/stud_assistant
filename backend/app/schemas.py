from pydantic import BaseModel, EmailStr, Field

# Shared properties
class UserBase(BaseModel):
    email: EmailStr = Field(min_length=5, max_length=120)
    username: str = Field(min_length=3, max_length=50)
    is_active: bool = True
    is_superuser: bool = False

# For creating a new user (input)
class UserCreate(UserBase):
    password: str  

# For returning user data (output)
class UserRead(UserBase):
    id: int

    class Config:
        orm_mode = True  

# For login
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str 

class TokenData(BaseModel):
    username: str | None = None