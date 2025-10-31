from dotenv import load_dotenv
from uuid import UUID
# JWT configuration

# in seconds
TOKEN_EXPIRE_TIME = 3600
SECRET_KEY = str(load_dotenv('SECRET_KEY'))
ALGORITHM = 'HS256'
SYSTEM_ID = UUID("00000000-0000-0000-0000-000000000001")
