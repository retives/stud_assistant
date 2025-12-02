from dotenv import load_dotenv
from uuid import UUID
import os
# JWT configuration

# in seconds
TOKEN_EXPIRE_TIME = 3600
SECRET_KEY = str(load_dotenv('SECRET_KEY'))
ALGORITHM = 'HS256'
SYSTEM_ID = UUID(os.getenv('SYSTEM_ID'))
SYSTEM_PASSWORD = os.getenv('SYSTEM_PASSWORD')
