from fastapi import APIRouter, Response, Depends, Path, HTTPException
from uuid import UUID, uuid4
import uuid
from typing import Annotated
from starlette import status
from app.database import db_dependency
from app.schemas import UserLogin, UserRead, UserCreate
from app.models import User
from app.database import get_db
from app.security import verify_password, hash_password, create_access_token, is_password_strong, read_access_token
from app.schemas import Token
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

# Router for auth module
router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_user_by_username(username: str, db) -> User:
    return db.query(User).filter(User.username == username).first()
    
# Authentication for login
def authenticate_user(username:str, password:str, db: db_dependency) -> User:
    db_user = get_user_by_username(username, db)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not verify_password(password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return db_user


# current user
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: db_dependency): # type: ignore
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        
        payload = read_access_token(token)
        print(payload)
        username: str = payload.get("username")
        if username is None:
            raise credentials_exception
    except Exception:
        raise credentials_exception
    
    user = get_user_by_username(username=username, db=db)
    
    if user is None:
        raise credentials_exception
    return user

# Register
@router.post('/signup')
async def register_user(user_request: UserCreate, db: db_dependency): # type: ignore
    # Password validation
    password = user_request.password

    if not is_password_strong(password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password is not strong enough. It must be at least 8 characters long and include uppercase letters, lowercase letters, numbers, and special characters.",
        )
    # User for DB
    user = User(
        id = str(uuid4()),
        username = user_request.username,
        email = user_request.email,
        password = hash_password(user_request.password),
        is_active = user_request.is_active,
        is_verified = True,
        is_superuser = False
    )
    
    # DB actions
    db.add(user)
    db.commit()
    db.refresh(user)

    # Login logic
    token = create_access_token(
        data = {'username': user.username, 'id': str(user.id), 'email': user.email}
        )
    return Token(access_token = token, token_type = 'bearer')

# Login 
@router.post('/token',response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db:db_dependency): # type: ignore
    # User model
    user = authenticate_user(form_data.username, form_data.password, db)
    # Token creation
    token = create_access_token(
        data = {'username': user.username, 'id': str(user.id), 'email': user.email}
        )
    return Token(access_token = token, token_type = 'bearer')

# Logout
@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(response: Response):
    response.delete_cookie("access_token")
    return response    

# Temp routes
@router.delete('/delete-account', status_code=status.HTTP_200_OK)
async def delete_user(db: db_dependency, user_id: str, current_user: Annotated[User, Depends(get_current_user)]): # type: ignore
    user_to_delete = db.query(User).filter(User.id == user_id).first()
    if user_to_delete:
        db.delete(user_to_delete)
        db.commit()
    return {"message": "User deleted successfully"}


@router.get('/list-users', status_code=status.HTTP_200_OK)
async def list_users(db: db_dependency, current_user: Annotated[User, Depends(get_current_user)]): # type: ignore
    return db.query(User).all()

@router.get('/user/{user_id}', status_code=status.HTTP_200_OK)
async def get_user(db: db_dependency, user_id: str, current_user: Annotated[User, Depends(get_current_user)]): # type: ignore
    return db.query(User).filter(User.id == user_id).first()

@router.get('/users/me', response_model=UserRead)
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)], db: db_dependency): # type: ignore
    return current_user