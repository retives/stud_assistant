from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from app.database import db_dependency
from app.schemas import ConversationNew, ConversationRead, ConversationMessages,MessageSave, ConversationUpdate, MessageCreate
from app.models import Conversation, Message
from typing import List
from app.routes.auth import get_current_user
from app.llm.agent import stud_agent
from app.config import SYSTEM_ID
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

@router.delete('/conversations/{conversation_id}/delete')
async def delete_conversation(db: db_dependency, 
                              conversation_id: str,
                              current_user = Depends(get_current_user), 
                              ):
    """
    Input: 
        - conversation_id:str (Query parameter)
        - body: None
    Output:
        - JsonResponse(201)
    """

    chat_to_delete = (db.query(Conversation)
                      .filter(Conversation.owner_id == current_user.id, Conversation.id == conversation_id)
                      ).first()
    if not chat_to_delete:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    try:
        db.delete(chat_to_delete)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete conversation")
        
    return JSONResponse(
        content='Deleted successfully',
        status_code=status.HTTP_200_OK
    )
# Get covnersation details
@router.get('/conversations/{conversation_id}', response_model=ConversationMessages)
async def get_conversation(conversation_id:str, 
                           db:db_dependency, 
                           current_user = Depends(get_current_user)
                           ):
    """
    Input: 
        - conversation_id: str - Query parameter
        - body: None 
    """
    # Conversation from the database
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
    print(conv_messages)
    return conv_messages


@router.put('/conversations/{conversation_id}')
async def update_conversation(updated_conversation: ConversationUpdate,
                              db: db_dependency, 
                              current_user = Depends(get_current_user)
                              ):
    """
    Input:
        - conversation_id: str - Query parameter
        - body: ConversationUpdate(title)
    Else is handled by FastAPI
    """

    conv_to_update = (db.query(Conversation)
    .filter(Conversation.id == updated_conversation.id, Conversation.owner_id == current_user.id)
    .first()
    )
    if not conv_to_update:
        raise HTTPException(status_code=404)
    
    conv_to_update.title = updated_conversation.title
    conv_to_update.date_changed = datetime.now(timezone.utc).replace(microsecond=0)
    db.commit()
    db.refresh(conv_to_update)
    
    return ConversationRead(conv_to_update)

# Send message
@router.post('/conversations/{conversation_id}/sendmessage', response_model=MessageSave)
async def send_message(
    conversation_id:str, 
    message_request: MessageCreate, 
    db:db_dependency, 
    current_user = Depends(get_current_user)
    ):
    """
    Endpoint for sending a message
    Input:
        - conversation_id: str - Query parameter
        - body: {MessageCreate(message_content)}
    Else is handled by FastAPI
    """
    # Getting the conversation
    conv = (db.query(Conversation)
    .filter(Conversation.id == conversation_id, Conversation.owner_id == current_user.id)
    .first()
    )
    if not conv:
        raise HTTPException(status_code=404)
    # Forming a user's message model
    message_content = message_request.message_content

    new_message = Message(
        id = str(uuid4()),
        content = message_content,
        date = datetime.now(timezone.utc).replace(microsecond=0),
        conversation_id = conversation_id,
        sender_id = str(current_user.id)
    )

    # --- User data (remove later)---
    courses = [''],
    faculty = 'Факультет інформаційних технологій',
    department = 'Інженерія програмного забезпечення',
    group = 'ІП-22-1',

    # Initializing student data
    stud_agent.update_user_info(courses, faculty, department, group)
    # Generating response
    response = stud_agent.ask(message_content)
    print(response)
    # Assigning title if needed
    if conv.title == "New chat":
        new_title = stud_agent.get_title(message_content)
        conv.title = new_title

    # Save Ai message
    message_from_ai = Message(
        id = str(uuid4()),
        content = response,
        date = datetime.now(timezone.utc).replace(microsecond=0),
        conversation_id = conversation_id,
        sender_id = SYSTEM_ID
    )


    db.add(new_message)
    db.add(message_from_ai)
    conv.date_changed = datetime.now(timezone.utc).replace(microsecond=0)
    db.commit()
    db.refresh(new_message)
    return message_from_ai



