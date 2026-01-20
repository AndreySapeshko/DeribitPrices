import asyncio
import os

import pytest
import pytest_asyncio
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.db.models import Base

load_dotenv()
POSTGRES_USER = os.environ.get("POSTGRES_USER", default="my_username")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", default="my_password")

TEST_DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:" f"{POSTGRES_PASSWORD}@localhost:5432/test_db"


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def engine():
    engine = create_async_engine(TEST_DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest.fixture
def sessionmaker(engine):
    return async_sessionmaker(
        bind=engine,
        expire_on_commit=False,
    )


@pytest.fixture
async def session(sessionmaker):
    session_factory = sessionmaker
    async with session_factory() as session:
        yield session
