from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://antonuricin@localhost:5432/mydb"
)

engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    poolclass=NullPool
)

async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_session():
    session = async_session()
    try:
        yield session
    finally:
        await session.close() 