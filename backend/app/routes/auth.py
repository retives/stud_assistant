from fastapi import APIRouter, Response, Depends, Path, HTTPException
from uuid import UUID
from typing import Annotated
from starlette import status
from app.database import db_dependency
from app.schemas import UserLogin, UserRead, UserCreate
from app.models import User
from app.database import get_db
from app.security import verify_password, hash_password, create_access_token
from app.schemas import Token
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# Router for auth module
router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# Authentication for login
def authenticate_user(username:str, password:str, db):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not verify_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
# current user
# !!! import oauth2 scheme !!!
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    pass
@router.post('/signup')
async def register_user(user_request: UserCreate):

    user = UserCreate(
        username = user_request.username,
        email = user_request.email,
        password = hash_password(user_request.password),
        is_active = user_request.is_active,
        is_verified = True,
        is_superuser = False
    )
    db.add(user)
    db.commit()

# Login
@router.post('/token', status_code = status.HTTP_200_OK)
async def login_for_access_token(user_request: UserCreate, db:db_dependency):
    user = authenticate_user(user_request.username, user_request.password, db)
    
    token = create_access_token(
        data = {'username': user.username, 'id': user.id, 'email': user.email}
        )
    # Errors
    return Token(access_token = token, token_type = 'bearer')

    



@router.delete('/delete-account', status_code=status.HTTP_200_OK)
async def delete_user(db: db_dependency, user_id: str):
    db.delete(User.id == user_id)


@router.get('/list-users', status_code=status.HTTP_200_OK)
async def list_users(db: db_dependency):
    return db.query(User).all()

@router.get('/user/{user_id}', status_code=status.HTTP_200_OK)
async def get_user(db: db_dependency, user_id: str):
    return db.query(User).filter(User.id == user_id).first()

