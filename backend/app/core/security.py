from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import APIRouter
from app.core.config import settings
from fastapi_users.authentication import CookieTransport

# Provides context of how to hash the password
pwd_context = CryptContext(schemes=['bcrypt'], dedprecated = 'auto')
# Same for generatin tokens 
# *Handle the '/token' route*
oauth2_context = OAuth2PasswordBearer(tokenUtl = 'token')
def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)



