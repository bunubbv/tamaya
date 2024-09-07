from sqlalchemy import text, func, select, insert, update, delete, or_
from sqlalchemy.exc import OperationalError, SQLAlchemyError, DatabaseError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.dialects.sqlite import Insert
from sqlalchemy.orm import sessionmaker

from core.schema import Config
from core.models import Base

engine = create_async_engine(Config.DBURL, echo=Config.DBECHO)
session = sessionmaker(
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    bind=engine,
)

async def connect_database() -> None:
    async with engine.begin() as conn:
        await conn.execute(text("PRAGMA journal_mode=WAL;"))
        await conn.execute(text("PRAGMA busy_timeout=5000;"))
        await conn.run_sync(Base.metadata.create_all)


async def disconnect_database() -> None:
    await engine.dispose()