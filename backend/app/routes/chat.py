from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from app.database import db_dependency
from app.schemas import ConversationNew, ConversationRead, ConversationMessages,MessageSave
from app.models import Conversation, Message
from typing import List
from app.routes.auth import get_current_user
from uuid import UUID, uuid4
import uuid
from datetime import datetime, timezone
router = APIRouter()

@router.post('/conversations/new-conversation')
def create_conversation(db: db_dependency, current_user = Depends(get_current_user)):
    # Create conversation in db
    new_conv = Conversation(
        title='New chat',
        owner_id = str(current_user.id),
        id = str(uuid4()),
        date_changed=datetime.now(timezone.utc).replace(microsecond=0)
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

@router.delete('/conversations/delete')
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

@router.get('/conversations/{conversation_id}', response_model=ConversationMessages)
async def get_conversation(conversation_id:str, db:db_dependency, current_user = Depends(get_current_user)):
    # Conversation fromthe database
    conv_to_open = (db.query(Conversation)
    .filter(Conversation.id == conversation_id, Conversation.owner_id == current_user.id)
    .first()
    )
    if not conv_to_open:
        raise HTTPException(status_code=404)
    print(conv_to_open)
    # Get the messages
    messages = (db.query(Message)
    .filter(Message.conversation_id == conversation_id))

    message_list = [MessageSave.model_validate(msg) for msg in messages]

    conv_messages = ConversationMessages(
        conversation= ConversationRead.model_validate(conv_to_open),
        messages=message_list
    )
    return conv_messages


@router.put('/conversations/{conversation_id}')
async def update_conversation(conversation_id:str, updated_conversation:ConversationNew, 
                              db: db_dependency, current_user = Depends(get_current_user)):
    conv_to_update = (db.query(Conversation)
    .filter(Conversation.id == conversation_id, Conversation.owner_id == current_user.id)
    .first()
    )
    if not conv_to_update:
        raise HTTPException(status_code=404)
    
    conv_to_update.title = updated_conversation.title
    conv_to_update.date_changed = datetime.now(timezone.utc).replace(microsecond=0)
    db.commit()
    db.refresh(conv_to_update)
    
    return conv_to_update

@router.post('/conversations/{conversation_id}/send_message', response_model=MessageSave)
async def send_message(conversation_id:str, message_content:str, db:db_dependency, current_user = Depends(get_current_user)):
    conv = (db.query(Conversation)
    .filter(Conversation.id == conversation_id, Conversation.owner_id == current_user.id)
    .first()
    )
    if not conv:
        raise HTTPException(status_code=404)
    
    new_message = Message(
        id = str(uuid4()),
        content = message_content,
        date = datetime.now(timezone.utc).replace(microsecond=0),
        conversation_id = conversation_id,
        sender_id = str(current_user.id)
    )

    db.add(new_message)
    conv.date_changed = datetime.now(timezone.utc).replace(microsecond=0)
    db.commit()
    db.refresh(new_message)
    return new_message



