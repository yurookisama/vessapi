from beanie import Document
from pydantic import Field
from datetime import datetime, date
from typing import List, Optional
from uuid import UUID, uuid4

class Music(Document):
    music_id: UUID = Field(default_factory=uuid4, unique=True)
    title: str
    artist_ids: List[UUID] = []
    duration: int
    file_path: str
    genre: Optional[str] = None
    track_number: Optional[int] = None
    publish_date: datetime
    lyrics: Optional[str] = None
    album_id: Optional[UUID] = None
    cover_image_url: Optional[str] = None
    owner_id: UUID
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "music"

class Album(Document):
    album_id: UUID = Field(default_factory=uuid4, unique=True)
    title: str
    artist_id: UUID
    release_date: date
    cover_image_url: str
    genre: Optional[str] = None
    description: Optional[str] = None
    music_ids: List[UUID] = []
    owner_id: UUID
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "albums"

from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"

class User(Document):
    user_id: UUID = Field(default_factory=uuid4, unique=True)
    username: str = Field(..., unique=True)
    full_name: Optional[str] = None
    hashed_password: str
    is_active: bool = True
    role: UserRole = UserRole.USER
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "users"

class Playlist(Document):
    playlist_id: UUID = Field(default_factory=uuid4, unique=True)
    name: str
    description: Optional[str] = None
    music_ids: List[UUID] = []
    is_public: bool = False
    owner_id: UUID
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "playlists"

class Artist(Document):
    artist_id: UUID = Field(default_factory=uuid4, unique=True)
    name: str = Field(..., unique=True)
    bio: Optional[str] = None
    image_url: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "artists"

__beanie_models__ = [Music, Album, User, Playlist, Artist]
