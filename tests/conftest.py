import pytest
import asyncio
from typing import AsyncGenerator

from fastapi import FastAPI, Depends
from httpx import AsyncClient, ASGITransport
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

# Import the main app instance
from main import app as main_app
from vessapi.models import __beanie_models__
import os

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="function")
async def client() -> AsyncGenerator[AsyncClient, None]:
    """
    Fixture that initializes a test database and yields an AsyncClient for the main app.
    """
    db_url = os.getenv("DATABASE_URL", "mongodb://localhost:27017/vessapi_test")
    db_client = AsyncIOMotorClient(db_url)
    
    await init_beanie(
        database=db_client.get_default_database(),
        document_models=__beanie_models__
    )

    # Create a test app instance without the startup event
    test_app = FastAPI(
        title="Test VessAPI",
        description="API service for music applications to sync music, albums, users, and playlists.",
        version="1.0.0"
    )

    # Manually include routers and other components from main_app
    test_app.include_router(main_app.router)
    for router in main_app.routes:
        if hasattr(router, 'router') and router.router is not None:
            test_app.include_router(router.router)

    transport = ASGITransport(app=test_app)
    async with AsyncClient(transport=transport, base_url="http://test") as test_client:
        yield test_client

    # Clean up the database after each test
    await db_client.drop_database(db_client.get_default_database())