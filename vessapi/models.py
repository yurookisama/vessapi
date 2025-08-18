from beanie import Document
from pydantic import EmailStr, Field
from datetime import datetime, date
from typing import List, Optional
from uuid import UUID, uuid4

class Music(Document):
    music_id: UUID = Field(default_factory=uuid4, unique=True)
    title: str
    artist_ids: List[UUID] = [] # Changed from 'artists' to 'artist_ids' and type to List[UUID]
    duration: int # in seconds
    file_path: str
    genre: Optional[str] = None
    track_number: Optional[int] = None
    publish_date: datetime
    lyrics: Optional[str] = None
    album_id: Optional[UUID] = None
    cover_image_url: Optional[str] = None # New field for music cover image
    owner_id: UUID # Added owner_id
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "music"

class Album(Document):
    album_id: UUID = Field(default_factory=uuid4, unique=True)
    title: str
    artist_id: UUID # Changed from 'artist' to 'artist_id' and type to UUID
    release_date: date
    cover_image_url: str
    genre: Optional[str] = None
    description: Optional[str] = None
    music_ids: List[UUID] = []
    owner_id: UUID # Added owner_id
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "albums"

class User(Document):
    user_id: UUID = Field(default_factory=uuid4, unique=True)
    username: str = Field(..., unique=True)
    email: EmailStr = Field(..., unique=True)
    hashed_password: str
    full_name: Optional[str] = None
    is_active: bool = True
    role: str = "user" # Added role field with default value
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "users"

class Playlist(Document):
    playlist_id: UUID = Field(default_factory=uuid4, unique=True)
    name: str
    description: Optional[str] = None
    user_id: UUID
    music_ids: List[UUID] = []
    is_public: bool = False
    owner_id: UUID # Added owner_id
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
