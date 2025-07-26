# src/db/session.py
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from src.config import DATABASE_URL
from contextlib import asynccontextmanager

# Use async engine
engine = create_async_engine(DATABASE_URL, echo=True)  # echo=True for debug logs

async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session

@asynccontextmanager
async def get_db_context() -> AsyncSession:
    session = async_session()
    try:
        yield session
        await session.commit()
    except:
        await session.rollback()
        raise
    finally:
        await session.close()