from fastapi import APIRouter, Form, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.models import User
from app.api.schemas.user import UserCreate, UserLogin, UserResponse
from uuid import uuid4
import re

router = APIRouter()

# @router.post('/auth/signup/', tags=['authentication'])
# async def signup(user: UserCreate, db: Session = Depends(get_db)):

#     existing = db.query(User).filter(
#         (User.username == user.username) | (User.email == user.email)
#     ).first()
#     if existing:
#         raise HTTPException(status_code=400, detail="User already exists")

#     if len(user.username) < 3 or len(user.username) > 50:
#         raise HTTPException(status_code=400, detail="Username must be 3-50 characters long")

#     if len(user.password) < 8 or len(user.password) > 255:
#         raise HTTPException(status_code=400, detail="Password must be 8-255 characters long")

#     if user.password != user.repeat_password:
#         raise HTTPException(status_code=400, detail="Passwords don't match")

#     if len(user.password) < 8 or not re.search(r"[A-Za-z]", user.password) or not re.search(r"\d", user.password):
#         raise HTTPException(status_code=400, detail="Password too weak")

#     # from app.core.security import hash_password

#     # hashed_pw = hash_password(user.password)
#     new_user = User(id = uuid4(), username=user.username, email=user.email, hashed_password=user.password)
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)

#     return user
# @router.post("/auth/login/")
# async def login(user: UserLogin, db = Depends(get_db)):
#     print("")