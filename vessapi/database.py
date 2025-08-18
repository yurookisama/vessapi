from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from typing import Optional
from pydantic import BaseModel

class Settings(BaseModel):
    DATABASE_URL: Optional[str] = "mongodb://localhost:27017"
    DATABASE_NAME: Optional[str] = "vessapi"

    class Config:
        env_file = ".env"

settings = Settings()

async def init_db():
    client = AsyncIOMotorClient(settings.DATABASE_URL)
    await init_beanie(
        database=client.get_database(settings.DATABASE_NAME),
        document_models=[
            "vessapi.models.Music",
            "vessapi.models.Album",
            "vessapi.models.User",
            "vessapi.models.Playlist",
            "vessapi.models.Artist", # New Artist model added
        ]
    )