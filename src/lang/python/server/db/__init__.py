from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlmodel import SQLModel

from server.config import settings

ENV = settings.FASTAPI_ENV == "development" 
DB_URL = settings.DEV_DATABASE_URL if ENV else settings.PROD_DATABASE_URL

db_engine = create_async_engine(
    url=DB_URL,
    echo=ENV,
)

async def create_db():
    async with db_engine.begin() as connection:
        #NOTE: Import all table models here to avoid circular imports:
        from user.schema import User

        await connection.run_sync(SQLModel.metadata.create_all)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async_session = async_sessionmaker(
        db_engine, 
        expire_on_commit=False)

    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()


