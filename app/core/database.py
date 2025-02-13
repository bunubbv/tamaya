from fastapi import HTTPException
from sqlalchemy import text, func, select, insert, update, delete, or_, and_, join, exists
from sqlalchemy.exc import OperationalError, SQLAlchemyError, DatabaseError, NoResultFound
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncConnection
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.dialects.sqlite import Insert
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from core.config import Config
from core.logging import logs

Base = declarative_base()
engine = create_async_engine(Config.DBURL, echo=Config.DBECHO)

session = sessionmaker(
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    bind=engine,
)

@asynccontextmanager
async def db_conn() -> AsyncGenerator[AsyncSession, None]:
    async with session() as conn:
        try:
            yield conn
            await conn.commit()

        except Exception as error:
            if not isinstance(error, HTTPException):
                logs.error("Error occurred: %s", error)
                await conn.rollback()
            raise


async def connect_database() -> None:
    async with engine.begin() as conn:
        await conn.execute(text("PRAGMA journal_mode=WAL;"))
        await conn.execute(text("PRAGMA busy_timeout=5000;"))
        await conn.run_sync(Base.metadata.create_all)


async def disconnect_database() -> None:
    await engine.dispose()
