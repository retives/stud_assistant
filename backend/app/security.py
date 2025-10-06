from passlib.context import CryptContext
from dotnev import load_dotenv

# Password generation context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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
