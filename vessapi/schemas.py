from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import List, Optional
from uuid import UUID

# Base Schemas (Ortak alanlar)
class BaseSchema(BaseModel):
    class Config:
        from_attributes = True

# Music Schemas
class MusicBase(BaseModel):
    title: str
    artist_ids: List[UUID] # Changed from 'artists' to 'artist_ids' and type to List[UUID]
    duration: int # in seconds
    file_path: str
    genre: Optional[str] = None
    track_number: Optional[int] = None
    publish_date: datetime
    lyrics: Optional[str] = None
    album_id: Optional[UUID] = None
    cover_image_url: Optional[str] = None # New field for music cover image

class MusicCreate(MusicBase):
    class Config:
        json_schema_extra = {
            "example": {
                "title": "Sample Song",
                "artist_ids": ["a1b2c3d4-e5f6-7890-1234-567890abcdef"],
                "duration": 240,
                "file_path": "/library/music/sample_song.mp3",
                "genre": "Pop",
                "track_number": 1,
                "publish_date": "2023-01-15T00:00:00Z",
                "lyrics": "Sample lyrics here...",
                "album_id": "f1e2d3c4-b5a6-9876-5432-10fedcba9876",
                "cover_image_url": "/library/images/music_image/sample_cover.png"
            }
        }

class MusicUpdate(MusicBase):
    title: Optional[str] = None
    artist_ids: Optional[List[UUID]] = None # Changed from 'artists' to 'artist_ids' and type to List[UUID]
    duration: Optional[int] = None
    file_path: Optional[str] = None
    publish_date: Optional[datetime] = None
    cover_image_url: Optional[str] = None
    class Config:
        json_schema_extra = {
            "example": {
                "title": "Updated Song Title",
                "genre": "Rock"
            }
        }

class MusicResponse(MusicBase):
    music_id: UUID
    created_at: datetime
    updated_at: datetime
    artist_names: List[str] = [] # Added for display purposes
    class Config:
        json_schema_extra = {
            "example": {
                "music_id": "12345678-1234-5678-1234-567890abcdef",
                "title": "Sample Song",
                "artist_ids": ["a1b2c3d4-e5f6-7890-1234-567890abcdef"],
                "duration": 240,
                "file_path": "/library/music/sample_song.mp3",
                "genre": "Pop",
                "track_number": 1,
                "publish_date": "2023-01-15T00:00:00Z",
                "lyrics": "Sample lyrics here...",
                "album_id": "f1e2d3c4-b5a6-9876-5432-10fedcba9876",
                "cover_image_url": "/library/images/music_image/sample_cover.png",
                "created_at": "2023-01-15T10:00:00Z",
                "updated_at": "2023-01-15T10:00:00Z"
            }
        }

# Album Schemas
class AlbumBase(BaseModel):
    title: str
    artist_id: UUID # Changed from 'artist' to 'artist_id' and type to UUID
    release_date: date
    cover_image_url: str
    genre: Optional[str] = None
    description: Optional[str] = None

class AlbumCreate(AlbumBase):
    class Config:
        json_schema_extra = {
            "example": {
                "title": "Sample Album",
                "artist_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
                "release_date": "2023-03-01",
                "cover_image_url": "/library/images/album_image/sample_album_cover.png",
                "genre": "Pop",
                "description": "A collection of sample songs."
            }
        }

class AlbumUpdate(AlbumBase):
    title: Optional[str] = None
    artist_id: Optional[UUID] = None # Changed from 'artist' to 'artist_id' and type to UUID
    release_date: Optional[date] = None
    cover_image_url: Optional[str] = None
    class Config:
        json_schema_extra = {
            "example": {
                "title": "Updated Album Title",
                "genre": "Rock"
            }
        }

class AlbumResponse(AlbumBase):
    album_id: UUID
    music_ids: List[UUID]
    num_tracks: int 
    artist_name: Optional[str] = None # Added for display purposes
    created_at: datetime
    updated_at: datetime
    class Config:
        json_schema_extra = {
            "example": {
                "album_id": "f1e2d3c4-b5a6-9876-5432-10fedcba9876",
                "title": "Sample Album",
                "artist_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
                "release_date": "2023-03-01",
                "cover_image_url": "/library/images/album_image/sample_album_cover.png",
                "genre": "Pop",
                "description": "A collection of sample songs.",
                "music_ids": ["12345678-1234-5678-1234-567890abcdef"],
                "num_tracks": 1,
                "artist_name": "Sample Artist",
                "created_at": "2023-03-01T10:00:00Z",
                "updated_at": "2023-03-01T10:00:00Z"
            }
        }

# User Schemas
class UserBase(BaseModel):
    username: str
    full_name: Optional[str] = None
    is_active: Optional[bool] = True
    role: Optional[str] = "user" # Added role field

class UserCreate(UserBase):
    password: str
    class Config:
        json_schema_extra = {
            "example": {
                "username": "testuser",
                "password": "securepassword",
                "full_name": "Test User",
                "is_active": True,
                "role": "user"
            }
        }

class UserUpdate(BaseModel):
    username: Optional[str] = None
    full_name: Optional[str] = None
    password: Optional[str] = None # Şifre güncelleme için
    is_active: Optional[bool] = None
    role: Optional[str] = None # Added role field
    class Config:
        json_schema_extra = {
            "example": {
                "full_name": "Updated User Name",
                "is_active": False
            }
        }

class UserResponse(UserBase):
    user_id: UUID
    created_at: datetime
    updated_at: datetime
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
                "username": "testuser",
                "full_name": "Test User",
                "is_active": True,
                "role": "user",
                "created_at": "2023-01-01T10:00:00Z",
                "updated_at": "2023-01-01T10:00:00Z"
            }
        }

# Playlist Schemas
class PlaylistBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_public: Optional[bool] = False

class PlaylistCreate(PlaylistBase):
    class Config:
        json_schema_extra = {
            "example": {
                "name": "My Top Hits",
                "description": "My favorite songs.",
                "is_public": True
            }
        }

class PlaylistUpdate(PlaylistBase):
    name: Optional[str] = None
    is_public: Optional[bool] = None
    class Config:
        json_schema_extra = {
            "example": {
                "name": "My New Top Hits",
                "is_public": False
            }
        }

class PlaylistResponse(PlaylistBase):
    playlist_id: UUID
    owner_id: UUID
    music_ids: List[UUID]
    created_at: datetime
    updated_at: datetime
    class Config:
        json_schema_extra = {
            "example": {
                "playlist_id": "b2c3d4e5-f6a7-8901-2345-67890abcdef1",
                "name": "My Top Hits",
                "description": "My favorite songs.",
                "is_public": True,
                "owner_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
                "music_ids": ["12345678-1234-5678-1234-567890abcdef"],
                "created_at": "2023-04-01T10:00:00Z",
                "updated_at": "2023-04-01T10:00:00Z"
            }
        }

# Artist Schemas
class ArtistBase(BaseModel):
    name: str
    bio: Optional[str] = None
    image_url: Optional[str] = None

class ArtistCreate(ArtistBase):
    class Config:
        json_schema_extra = {
            "example": {
                "name": "New Artist",
                "bio": "A talented musician.",
                "image_url": "/library/images/artist_image/new_artist.png"
            }
        }

class ArtistUpdate(ArtistBase):
    name: Optional[str] = None
    bio: Optional[str] = None
    image_url: Optional[str] = None
    class Config:
        json_schema_extra = {
            "example": {
                "bio": "An even more talented musician."
            }
        }

class ArtistResponse(ArtistBase):
    artist_id: UUID
    created_at: datetime
    updated_at: datetime
    class Config:
        json_schema_extra = {
            "example": {
                "artist_id": "c3d4e5f6-a7b8-9012-3456-7890abcdef12",
                "name": "New Artist",
                "bio": "A talented musician.",
                "image_url": "/library/images/artist_image/new_artist.png",
                "created_at": "2023-05-01T10:00:00Z",
                "updated_at": "2023-05-01T10:00:00Z"
            }
        }


