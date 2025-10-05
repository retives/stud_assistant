from fastapi import APIRouter, Response, Depends, Path, HTTPException
from uuid import UUID
from typing import Annotated
from starlette import status
from app.database import db_dependency
from app.schemas import UserLogin, UserRead, UserCreate
from app.models import User
from app.database import get_db
from app.security import verify_password, hash_password
router = APIRouter()

def authenticate_user(username:str, password:str):
    user = User.filter(User.username == username).first()
    if not user:
        return HTTPException(status_code = 422, detail="Username doesn't exist")
    if not verify_password(password):
        return HTTPException(status_code = 422, detail="Password is incorrect")
    return Response(status_code = 200, detail = "Successful login")
@router.post('/signup')
def register_user(user_request: UserCreate):
    user = UserCreate(
        username = user_request.username,
        email = user_request.email,
        password = user_request.password,
        is_active = user_request.is_active
    )

    # Errors
    return {"error": "Invalid data"}

@router.post('/login', status_code = statuc.HTTP_200_OK)
def login_user(user_request: UserCreate, db = db_dependency):
    


    # Errors
    return {"error": "Invalid data"}

@router.post('/create-user', status_code=status.HTTP_201_CREATED)
def create_user(db: db_dependency, user_request: UserCreate):
    user_model = User(**user_request.dict())
    db.add(user_model)
    db.commit()
    # Errors
    return {"error": "Invalid data"}

@router.delete('/delete-account', status_code=status.HTTP_200_OK)
async def delete_user(db: db_dependency, user_id: str):
    db.delete(User.id == user_id)


@router.get('/list-users', status_code=status.HTTP_200_OK)
async def list_users(db: db_dependency):
    return db.query(User).all()

@router.get('/user/{user_id}', status_code=status.HTTP_200_OK)
async def get_user(db: db_dependency, user_id: str):
    return db.query(User).filter(User.id == user_id).first()