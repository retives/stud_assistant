from pydantic import BaseModel, EmailStr, Field, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional
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
class ConversationBase(BaseModel):
    owner_id: UUID
class ConversationNew(ConversationBase):
    pass 
class ConversationRead(ConversationBase):
    id: UUID
    title: str
    date_changed: datetime

    model_config = ConfigDict(from_attributes=True)
    
class ConversationUpdate(ConversationBase):
    title: str

class ConversationDelete(BaseModel):
    id: UUID
    
# Message schemas
class MessageBase(BaseModel):
    content: str
    conversation_id: UUID
    sender_id: UUID

class MessageSend(MessageBase):
    pass

class MessageSave(MessageBase):
    date: datetime
    model_config = ConfigDict(from_attributes=True)

class MessageCreate(BaseModel):
    message_content: str

class ConversationMessages(BaseModel):
    conversation: ConversationRead
    messages: list[MessageSave] | None = None
    
# Stripe

class CheckoutResponse(BaseModel):
    url: str
class PlanSelection(BaseModel):
    selected_plan: str