from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# Empty base for models
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    is_active = Column(Integer, default=1)
    is_verified = Column(Integer, default=0)
    is_superuser = Column(Integer, default=0)

    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}')>"
    
