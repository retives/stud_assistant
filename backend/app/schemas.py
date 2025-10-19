from pydantic import BaseModel, EmailStr, Field, ConfigDict
from uuid import UUID
from datetime import datetime as timestamp
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
    id: UUID

    model_config = ConfigDict(from_attributes=True)

# For login
class UserLogin(BaseModel):
    username: str
    password: str

# Token
class Token(BaseModel):
    access_token: str
    token_type: str 

class TokenData(BaseModel):
    username: str | None = None

# Conversation schema
class Conversation(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    owner_id: int
# Message schemas

class MessageSave(BaseModel):
    id: UUID
    content: str
    conversation_id: int
    date: timestamp

class MessageSend(BaseModel):
    content: str
    sender_id: UUID
    conversation_id: int
    