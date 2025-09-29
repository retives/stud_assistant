import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from fastapi import APIRouter, Depends
from app.models import Base
from sqlalchemy import text
import asyncio
# Database connection string
DATABASE_URL= 'postgresql+psycopg2://stud_user:student@localhost:5432/stud_assistant'

engine = sa.create_engine(DATABASE_URL, echo=True, future=True)
Session = sessionmaker(bind=engine, expire_on_commit=False)

# user_router
router = APIRouter()

def create_tables():
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    create_tables()