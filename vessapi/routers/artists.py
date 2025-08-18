from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from uuid import UUID

from vessapi import crud, schemas, models
from vessapi.auth import get_current_active_user

router = APIRouter(
    prefix="/artists",
    tags=["artists"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=schemas.ArtistResponse, status_code=status.HTTP_201_CREATED, summary="Create a new artist", description="Creates a new artist with the provided details.")
async def create_artist_api(artist: schemas.ArtistCreate, current_user: models.User = Depends(get_current_active_user)):
    db_artist = await crud.get_artist_by_name(name=artist.name)
    if db_artist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Artist with this name already exists")
    return await crud.create_artist(artist=artist)

@router.get("/", response_model=List[schemas.ArtistResponse], summary="Retrieve all artists", description="Retrieves a list of all registered artists. Supports pagination.")
async def read_artists(skip: int = Query(0, ge=0, description="Number of items to skip"), limit: int = Query(100, ge=1, le=1000, description="Maximum number of items to return")):
    return await crud.get_artists(skip=skip, limit=limit)

@router.get("/{artist_id}", response_model=schemas.ArtistResponse, summary="Retrieve a single artist by ID", description="Retrieves a specific artist using their unique ID.")
async def read_artist(artist_id: UUID):
    db_artist = await crud.get_artist(artist_id=artist_id)
    if db_artist is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Artist not found")
    return db_artist

@router.put("/{artist_id}", response_model=schemas.ArtistResponse, summary="Update an existing artist", description="Updates an existing artist identified by their ID.")
async def update_artist_api(artist_id: UUID, artist: schemas.ArtistUpdate, current_user: models.User = Depends(get_current_active_user)):
    db_artist = await crud.update_artist(artist_id=artist_id, artist=artist)
    if db_artist is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Artist not found")
    return db_artist

@router.delete("/{artist_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete an artist", description="Deletes an artist identified by their ID.")
async def delete_artist_api(artist_id: UUID, current_user: models.User = Depends(get_current_active_user)):
    db_artist = await crud.delete_artist(artist_id=artist_id)
    if db_artist is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Artist not found")
    return

@router.get("/{artist_id}/music", response_model=List[schemas.MusicResponse], summary="Retrieve music by artist ID", description="Retrieves a list of music tracks by a specific artist ID. Supports pagination.")
async def get_music_by_artist_api(artist_id: UUID, skip: int = Query(0, ge=0, description="Number of items to skip"), limit: int = Query(100, ge=1, le=1000, description="Maximum number of items to return")):
    return await crud.get_music_by_artist_id(artist_id=artist_id, skip=skip, limit=limit)

@router.get("/{artist_id}/albums", response_model=List[schemas.AlbumResponse], summary="Retrieve albums by artist ID", description="Retrieves a list of albums by a specific artist ID. Supports pagination.")
async def get_albums_by_artist_api(artist_id: UUID, skip: int = Query(0, ge=0, description="Number of items to skip"), limit: int = Query(100, ge=1, le=1000, description="Maximum number of items to return")):
    albums = await crud.get_albums_by_artist_id(artist_id=artist_id, skip=skip, limit=limit)
    albums_with_artist_names = []
    for album in albums:
        album_dict = album.model_dump()
        album_dict["num_tracks"] = len(album.music_ids)
        artist = await crud.get_artist(album.artist_id)
        if artist:
            album_dict["artist_name"] = artist.name
        albums_with_artist_names.append(schemas.AlbumResponse(**album_dict))
    return albums_with_artist_names
