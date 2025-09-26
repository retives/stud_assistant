from pydantic import BaseModel
from uuid import UUID


class UserBase(BaseModel):
    email: str
    is_active: bool = True
    is_verified: bool = False
    is_superuser: bool = False
    
class UserCreate(UserBase):
    password: str

class UserLogin():
    password: str 
class UserRead(UserBase):
    id: int


