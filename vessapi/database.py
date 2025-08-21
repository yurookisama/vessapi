from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from vessapi.config import settings

async def init_db():
    """Veritabanını başlat"""
    client = AsyncIOMotorClient(settings.database.url)
    await init_beanie(
        database=client.get_database(settings.database.name),
        document_models=[
            "vessapi.models.Music",
            "vessapi.models.Album",
            "vessapi.models.User",
            "vessapi.models.Playlist",
            "vessapi.models.Artist",
        ]
    )