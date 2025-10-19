from fastapi import APIRouter, Depends, HTTPException, status
from app.database import db_dependency
from app.schemas import MessageCreate, Message

router = APIRouter()

@router.post('/send-message')
def send_mesasge(message_data: str db = db_dependency): # type: ignore
    pass
