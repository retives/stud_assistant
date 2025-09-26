from fastapi import APIRouter, Response
from typing import Union
from app.schemas import UserLogin, UserRead, UserCreate

router = APIRouter()

@router.post('/signup')
def register_user(user: UserCreate):
    email = user.email 
    password = user.password 

    # Validation logic
    if email and password:
        read_user = UserRead(email = email, id = 1)
        # Successful return
        return read_user
    # Errors
    return {"error": "Invalid data"}

@router.post('/login')
def login_user(user: UserCreate):
    email = user.email
    password = user.password

    # Validation logic

    if email and password:
        read_user = UserRead(email = email, id = 1)
        # Successful return
        return read_user
    # Errors
    return {"error": "Invalid data"}