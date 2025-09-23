from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from app.db.database import Base

class User(Base):

    __tablename__ = "users"

    id = Column(UUID, primary_key=True)
    username = Column(String(255), unique = True, nullable = False)
    email = Column(String(255), unique = True, nullable = False)
    hashed_password = Column(String(255), nullable = False)
    is_active = Column(Boolean, default = True)
    
