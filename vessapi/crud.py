from passlib.context import CryptContext
from typing import List, Optional
from uuid import UUID
from datetime import datetime, date

from vessapi.models import Music, Album, User, Playlist, Artist
from vessapi.schemas import (MusicCreate, MusicUpdate, 
                     AlbumCreate, AlbumUpdate,
                     UserCreate, UserUpdate,
                     PlaylistCreate, PlaylistUpdate,
                     ArtistCreate, ArtistUpdate)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Music CRUD
async def get_music(music_id: UUID) -> Optional[Music]:
    return await Music.find_one(Music.music_id == music_id)

async def get_music_all(
    skip: int = 0,
    limit: int = 100,
    title: Optional[str] = None,
    artist_ids: Optional[List[UUID]] = None,
    genre: Optional[str] = None,
    min_duration: Optional[int] = None,
    max_duration: Optional[int] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> List[Music]:
    query = {}
    if title:
        query["title"] = {"$regex": title, "$options": "i"}
    if artist_ids:
        query["artist_ids"] = {"$in": artist_ids}
    if genre:
        query["genre"] = {"$regex": genre, "$options": "i"}
    if min_duration is not None:
        query["duration"] = {"$gte": min_duration}
    if max_duration is not None:
        if "duration" in query:
            query["duration"]["$lte"] = max_duration
        else:
            query["duration"] = {"$lte": max_duration}
    if start_date:
        query["publish_date"] = {"$gte": start_date}
    if end_date:
        if "publish_date" in query:
            query["publish_date"]["$lte"] = end_date
        else:
            query["publish_date"] = {"$lte": end_date}

    return await Music.find(query).skip(skip).limit(limit).to_list()

async def create_music(music: MusicCreate, owner_id: UUID) -> Music:
    db_music = Music(**music.model_dump(), owner_id=owner_id)
    await db_music.insert()
    return db_music

async def update_music(music_id: UUID, music: MusicUpdate, owner_id: UUID, is_admin: bool = False) -> Optional[Music]:
    db_music = await get_music(music_id)
    if db_music and (db_music.owner_id == owner_id or is_admin):
        update_data = music.model_dump(exclude_unset=True)
        await db_music.update({"$set": update_data})
        return await get_music(music_id)
    return None

async def delete_music(music_id: UUID, owner_id: UUID, is_admin: bool = False) -> Optional[Music]:
    db_music = await get_music(music_id)
    if db_music and (db_music.owner_id == owner_id or is_admin):
        await db_music.delete()
        return db_music
    return None

# Album CRUD
async def get_album(album_id: UUID) -> Optional[Album]:
    return await Album.find_one(Album.album_id == album_id)

async def get_album_by_title_and_artist_id(title: str, artist_id: UUID) -> Optional[Album]:
    return await Album.find_one(Album.title == title, Album.artist_id == artist_id)

async def get_albums(
    skip: int = 0,
    limit: int = 100,
    title: Optional[str] = None,
    artist_id: Optional[UUID] = None,
    genre: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None
) -> List[Album]:
    query = {}
    if title:
        query["title"] = {"$regex": title, "$options": "i"}
    if artist_id:
        query["artist_id"] = artist_id
    if genre:
        query["genre"] = {"$regex": genre, "$options": "i"}
    if start_date:
        query["release_date"] = {"$gte": start_date}
    if end_date:
        if "release_date" in query:
            query["release_date"]["$lte"] = end_date
        else:
            query["release_date"] = {"$lte": end_date}

    return await Album.find(query).skip(skip).limit(limit).to_list()

async def create_album(album: AlbumCreate, owner_id: UUID) -> Album:
    db_album = Album(**album.model_dump(), owner_id=owner_id)
    await db_album.insert()
    return db_album

async def update_album(album_id: UUID, album: AlbumUpdate, owner_id: UUID, is_admin: bool = False) -> Optional[Album]:
    db_album = await get_album(album_id)
    if db_album and (db_album.owner_id == owner_id or is_admin):
        update_data = album.model_dump(exclude_unset=True)
        await db_album.update({"$set": update_data})
        return await get_album(album_id)
    return None

async def delete_album(album_id: UUID, owner_id: UUID, is_admin: bool = False) -> Optional[Album]:
    db_album = await get_album(album_id)
    if db_album and (db_album.owner_id == owner_id or is_admin):
        await db_album.delete()
        return db_album
    return None

# User CRUD
async def get_user(user_id: UUID) -> Optional[User]:
    return await User.find_one(User.user_id == user_id)

async def get_user_by_username(username: str) -> Optional[User]:
    return await User.find_one({"username": username})

async def get_users(skip: int = 0, limit: int = 100) -> List[User]:
    return await User.find_all().skip(skip).limit(limit).to_list()

async def create_user(user: UserCreate) -> User:
    hashed_password = get_password_hash(user.password)
    # Create a dictionary from the user model, excluding the password
    user_data = user.model_dump(exclude={"password"})
    
    # Ensure the role is always 'user' when creating through the public API
    user_data['role'] = 'user'

    db_user = User(
        **user_data,
        hashed_password=hashed_password
    )
    await db_user.insert()
    return db_user

async def update_user(user_id: UUID, user: UserUpdate) -> Optional[User]:
    db_user = await get_user(user_id)
    if db_user:
        update_data = user.model_dump(exclude_unset=True)
        if "password" in update_data and update_data["password"]:
            update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
        await db_user.update({"$set": update_data})
        return await get_user(user_id)
    return None

async def delete_user(user_id: UUID) -> Optional[User]:
    db_user = await get_user(user_id)
    if db_user:
        await db_user.delete()
        return db_user
    return None

# Playlist CRUD
async def get_playlist(playlist_id: UUID, user_id: Optional[UUID] = None) -> Optional[Playlist]:
    playlist = await Playlist.find_one(Playlist.playlist_id == playlist_id)
    if playlist:
        # Allow access if the playlist is public or if the user is the owner
        if playlist.is_public or (user_id and playlist.owner_id == user_id):
            return playlist
    return None

async def get_playlists(
    skip: int = 0, 
    limit: int = 100, 
    user_id: Optional[UUID] = None
) -> List[Playlist]:
    query = {
        "$or": [
            {"is_public": True},
            {"owner_id": user_id}
        ]
    }
    if user_id is None:
        # If no user is provided, only return public playlists
        query = {"is_public": True}
        
    return await Playlist.find(query).skip(skip).limit(limit).to_list()

async def create_playlist(playlist: PlaylistCreate, owner_id: UUID) -> Playlist:
    db_playlist = Playlist(**playlist.model_dump(), owner_id=owner_id)
    await db_playlist.insert()
    return db_playlist

async def update_playlist(playlist_id: UUID, playlist: PlaylistUpdate, owner_id: UUID) -> Optional[Playlist]:
    db_playlist = await get_playlist(playlist_id)
    if db_playlist and db_playlist.owner_id == owner_id:
        update_data = playlist.model_dump(exclude_unset=True)
        await db_playlist.update({"$set": update_data})
        return await get_playlist(playlist_id)
    return None

async def delete_playlist(playlist_id: UUID, owner_id: UUID) -> Optional[Playlist]:
    db_playlist = await get_playlist(playlist_id)
    if db_playlist and db_playlist.owner_id == owner_id:
        await db_playlist.delete()
        return db_playlist
    return None

# PlaylistMusic CRUD
async def add_music_to_playlist(playlist_id: UUID, music_id: UUID, owner_id: UUID) -> Optional[Playlist]:
    playlist = await get_playlist(playlist_id)
    music = await get_music(music_id)
    if playlist and music and playlist.owner_id == owner_id:
        await playlist.update({"$addToSet": {"music_ids": music_id}})
        return await get_playlist(playlist_id)
    return None

async def remove_music_from_playlist(playlist_id: UUID, music_id: UUID, owner_id: UUID) -> Optional[Playlist]:
    playlist = await get_playlist(playlist_id)
    music = await get_music(music_id)
    if playlist and music and playlist.owner_id == owner_id:
        await playlist.update({"$pull": {"music_ids": music_id}})
        return await get_playlist(playlist_id)
    return None

async def get_music_in_playlist(playlist_id: UUID) -> List[Music]:
    playlist = await get_playlist(playlist_id)
    if playlist:
        return await Music.find(Music.music_id.in_(playlist.music_ids)).to_list()
    return []

# Artist CRUD
async def get_artist(artist_id: UUID) -> Optional[Artist]:
    return await Artist.find_one(Artist.artist_id == artist_id)

async def get_artist_by_name(name: str) -> Optional[Artist]:
    return await Artist.find_one(Artist.name == name)

async def get_artists(skip: int = 0, limit: int = 100) -> List[Artist]:
    return await Artist.find_all().skip(skip).limit(limit).to_list()

async def create_artist(artist: ArtistCreate) -> Artist:
    db_artist = Artist(**artist.model_dump())
    await db_artist.insert()
    return db_artist

async def update_artist(artist_id: UUID, artist: ArtistUpdate) -> Optional[Artist]:
    db_artist = await get_artist(artist_id)
    if db_artist:
        update_data = artist.model_dump(exclude_unset=True)
        await db_artist.update({"$set": update_data})
        return await get_artist(artist_id)
    return None

async def delete_artist(artist_id: UUID) -> Optional[Artist]:
    db_artist = await get_artist(artist_id)
    if db_artist:
        await db_artist.delete()
        return db_artist
    return None

async def get_music_by_artist_id(artist_id: UUID, skip: int = 0, limit: int = 100) -> List[Music]:
    return await Music.find(Music.artist_ids == artist_id).skip(skip).limit(limit).to_list()

async def get_albums_by_artist_id(artist_id: UUID, skip: int = 0, limit: int = 100) -> List[Album]:
    return await Album.find(Album.artist_id == artist_id).skip(skip).limit(limit).to_list()

# Helper function to enrich album response with additional data
async def enrich_album_response(album: Album):
    from vessapi.schemas import AlbumResponse
    
    # Get artist name
    artist = await get_artist(album.artist_id)
    artist_name = artist.name if artist else "Unknown Artist"
    
    # Count tracks in album
    num_tracks = len(album.music_ids)
    
    return AlbumResponse(
        album_id=album.album_id,
        title=album.title,
        artist_id=album.artist_id,
        artist_name=artist_name,
        release_date=album.release_date,
        cover_image_url=album.cover_image_url,
        genre=album.genre,
        description=album.description,
        music_ids=album.music_ids,
        num_tracks=num_tracks,
        created_at=album.created_at,
        updated_at=album.updated_at
    )

# Helper function to enrich music response with additional data
async def enrich_music_response(music: Music):
    from vessapi.schemas import MusicResponse
    
    # Get artist names
    artist_names = []
    for artist_id in music.artist_ids:
        artist = await get_artist(artist_id)
        if artist:
            artist_names.append(artist.name)
    
    return MusicResponse(
        music_id=music.music_id,
        title=music.title,
        artist_ids=music.artist_ids,
        artist_names=artist_names,
        duration=music.duration,
        file_path=music.file_path,
        genre=music.genre,
        track_number=music.track_number,
        publish_date=music.publish_date,
        lyrics=music.lyrics,
        album_id=music.album_id,
        cover_image_url=music.cover_image_url,
        created_at=music.created_at,
        updated_at=music.updated_at
    )