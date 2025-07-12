from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
import os
import logging

logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    logger.error("❌ DATABASE_URL environment variable is not set!")
    raise ValueError("DATABASE_URL environment variable must be set")

logger.info(f"🔗 Подключение к БД: {DATABASE_URL[:50]}...")

# Railway предоставляет URL в формате postgresql://, но нам нужно postgresql+asyncpg://
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
    logger.info("🔄 Преобразован URL для asyncpg")

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