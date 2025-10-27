from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, UUID
from sqlalchemy.orm import declarative_base
# Empty base for models
Base = declarative_base()

# User model
class User(Base):
    __tablename__ = 'users'
    
    id = Column(UUID, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(255), nullable = False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)

    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}')>"

# Message model
# Foreign key to conversation
class Message(Base):
    __tablename__ = 'messages'

    id = Column(UUID, primary_key = True)
    content = Column(String)
    date = Column(DateTime)
    conversation_id = Column(UUID, ForeignKey('conversations.id'))
# Conversation model 
# Foreign key to user
class Conversation(Base):
    __tablename__ = 'conversations'

    id = Column(UUID, primary_key = True)
    title = Column(String(100))
    owner_id = Column(UUID, ForeignKey('users.id'))
    date_changed = Column(DateTime)
    
    