from fastapi import APIRouter, Depends, HTTPException, status
from app.database import db_dependency
from app.schemas import ConversationNew, ConversationRead
from app.models import Conversation
from typing import List
from app.routes.auth import get_current_user
from uuid import UUID, uuid5
import uuid
from datetime import datetime
router = APIRouter()

@router.post('/send-message')
def send_mesasge(message_data: str, db: db_dependency): # type: ignore
    pass
    
@router.post('/new-conversation')
def create_conversation(conversation: ConversationNew, db: db_dependency):
    
    # Create conversation in db
    new_conv = Conversation(
        title='New chat',
        owner_id = conversation.owner_id,
        id = uuid5(uuid.NAMESPACE_URL, 'http://localhost:8000'),
        date_changed=datetime.now()
    )
    db.add(new_conv)
    db.commit()
    return new_conv
# response_model=List[ConversationRead]
@router.get('/conversations')
def get_user_conversations(db: db_dependency, current_user = Depends(get_current_user)):
    conversations = (
    db.query(Conversation)
    .filter(Conversation.owner_id == current_user.id)
    .order_by(Conversation.date_changed)
    .all()
    )
    return conversations
