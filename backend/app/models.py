from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

# Empty base for models
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(255), nullable = False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)

    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}')>"


class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key = True)
    content = Column(String)
    date = Column(DateTime)
    conversation_id = Column(Integer, ForeignKey('conversations.id'))

class Conversation(Base):
    __tablename__ = 'conversations'

    id = Column(Integer, primary_key = True)
    title = Column(String(100))
    owner_id = Column(Integer, ForeignKey('users.id'))
    
