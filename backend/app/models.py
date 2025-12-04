from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, UUID, Enum, Float
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
# Empty base for models
Base = declarative_base()

# User model
class User(Base):
    __tablename__ = 'users'
    
    id = Column(UUID, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(255), nullable = False)
    customers_id = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)
    
    customer_id = Column(UUID)
    
    subscriptions = relationship("Subscription", back_populates="user")
    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}')>"

# Message model
# Foreign key to conversation
class Message(Base):
    __tablename__ = 'messages'

    id = Column(UUID, primary_key = True)
    content = Column(String)
    date = Column(DateTime)
    sender_id = Column(UUID, ForeignKey('users.id'))
    conversation_id = Column(
        UUID(as_uuid=True),
        ForeignKey("conversations.id", ondelete="CASCADE"),
        nullable=False
    )
    conversation = relationship("Conversation", back_populates="messages")
# Conversation model 
# Foreign key to user
class Conversation(Base):
    __tablename__ = 'conversations'

    id = Column(UUID, primary_key = True)
    title = Column(String(100))
    owner_id = Column(UUID, ForeignKey('users.id'))
    date_changed = Column(DateTime)
    messages = relationship(
        "Message",
        back_populates="conversation",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(UUID, primary_key=True, index=True)
    user_id = Column(UUID, ForeignKey("users.id"), nullable=False)
    stripe_subscription_id = Column(String, unique=True, nullable=False)
    price_id = Column(String, nullable=False)  
    status = Column(String, default="incomplete") 
    current_period_start = Column(DateTime, nullable=True)
    current_period_end = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.utcnow)

    user = relationship("User", back_populates="subscriptions")