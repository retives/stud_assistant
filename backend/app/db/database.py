from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from collections.abc import AsyncGenerator

# Database URL
DATABASE_URL = "postgresql+asyncpg://stud_user:student@localhost:5432/stud_assistant"


# Base class for ORM
class Base(DeclarativeBase):
    pass


# Engine and session
engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


# Dependency: DB session
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


# DB init (dev only — use Alembic in prod)
async def create_db_and_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
