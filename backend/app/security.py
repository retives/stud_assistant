from passlib.context import CryptContext
from datetime import timedelta, datetime
from app.config import TOKEN_EXPIRE_TIME, SECRET_KEY, ALGORITHM
import jwt
# Password generation context
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# Hashing
def hash_password(password: str) -> str:
    return pwd_context.hash(password)
# Veirfication against actual an hashed stored password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Password strongness verification
def is_password_strong(password: str) -> bool:
    if len(password) < 8:
        return False
    if not any(char.isdigit() for char in password):
        return False
    if not any(char.isupper() for char in password):
        return False
    if not any(char.islower() for char in password):
        return False
    if not any(char in "!@#$%^&*()-_=+[]{}|;:'\",.<>?/`~" for char in password):
        return False
    return True

def create_access_token(data:dict, expires_delta: timedelta = TOKEN_EXPIRE_TIME):
    to_encode = data.copy()

    expire_time = datetime.now() + expires_delta

    to_encode.update({'exp': expire_time})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)
    return encoded_jwt

def read_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception("Token has expired")
    except jwt.InvalidTokenError:
        raise Exception("Invalid token")

