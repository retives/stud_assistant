from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from app.db.database import db
from app.api.schemas.user import UserInDb
# Here are the methods responsible for handling oauth2 and generating tokens

router = APIRouter()


@router.get('/token')
def 




