import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Annotated
from sqlalchemy import text

from app.models import Base
# Database connection string
DATABASE_URL= 'postgresql+psycopg2://stud_user:student@db:5432/stud_assistant'

engine = sa.create_engine(DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

# user_router
router = APIRouter()

# Table creation
def create_tables():
    Base.metadata.create_all(engine)

# Session creation
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Input type for routes to ensure the integrity
db_dependency = Annotated[Session, Depends(get_db)]

if __name__ == '__main__':
    print(Base.metadata.tables.keys())
    from app.models import Base, Message
    print(Base.metadata.tables.keys())
    print(Message.__table__.columns.keys())
    import app.models
    print(app.models.__file__)

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)