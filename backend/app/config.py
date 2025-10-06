from dotenv import load_dotenv
# JWT configuration

# in seconds
TOKEN_EXPIRE_TIME = 3600
SECRET_KEY = load_dotenv('SECRET_KEY')
ALGORITHM = 'HS256'