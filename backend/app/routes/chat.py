from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from app.database import db_dependency
from app.schemas import ConversationNew, ConversationRead
from app.models import Conversation
from typing import List
from app.routes.auth import get_current_user
from uuid import UUID, uuid4
import uuid
from datetime import datetime
router = APIRouter()

@router.post('/new-conversation')
def create_conversation(conversation: ConversationNew, db: db_dependency):
    
    # Create conversation in db
    new_conv = Conversation(
        title='New chat',
        owner_id = conversation.owner_id,
        id = str(uuid4()),
        date_changed=datetime.now()
    )
    db.add(new_conv)
    db.commit()
    return new_conv

# 
@router.get('/conversations', response_model=List[ConversationRead])
def get_user_conversations(db: db_dependency, current_user = Depends(get_current_user)):
    conversations = (
    db.query(Conversation)
    .filter(Conversation.owner_id == current_user.id)
    .order_by(Conversation.date_changed)
    .all()
    )
    return conversations

@router.delete('/delete')
async def delete_conversation(db: db_dependency, current_user = Depends(get_current_user), chat_to_delete = ConversationNew):
    chat_to_delete = (db.query(Conversation)
                      .filter(Conversation.owner_id == current_user.id, Conversation.id == chat_to_delete.id)
                      )
    if chat_to_delete:
        try:
            db.delete(chat_to_delete)
            db.commit()
        except HTTPException:
            pass
    return JSONResponse(
        content='Deleted successfully',
        status_code=status.HTTP_201_CREATED 
    )

@router.get('/conversations/{conversation_id}')
async def get_conversation(conversation_id:str, db:db_dependency, current_user = Depends(get_current_user)):

    conv_to_open = (db.query(Conversation)
    .filter(Conversation.id == conversation_id, Conversation.owner_id == current_user.id)
    .first()
    )
    if not conv_to_open:
        raise HTTPException(status_code=404)
    print(conv_to_open)
    return ConversationRead(*conv_to_open)

