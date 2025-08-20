from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from uuid import UUID

from vessapi import crud, schemas, models
from vessapi.auth import has_role
from vessapi.models import UserRole, User

router = APIRouter(
    prefix="/artists",
    tags=["Artists"],
    responses={404: {"description": "Not found"}},
)

# Admin role dependency
is_admin = has_role([UserRole.ADMIN])

@router.post("/", response_model=schemas.ArtistResponse, status_code=status.HTTP_201_CREATED, summary="Create new artist (Admin only)")
async def create_artist_api(artist: schemas.ArtistCreate, admin: User = Depends(is_admin)):
    """
    Create a new artist entry. Requires admin privileges.
    """
    db_artist = await crud.get_artist_by_name(name=artist.name)
    if db_artist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Artist with this name already exists")
    return await crud.create_artist(artist=artist)

@router.get("/", response_model=List[schemas.ArtistResponse], summary="Retrieve all artists")
async def read_artists(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1)):
    """
    Retrieve a list of all registered artists. This endpoint is public.
    """
    return await crud.get_artists(skip=skip, limit=limit)

@router.get("/{artist_id}", response_model=schemas.ArtistResponse, summary="Retrieve a single artist by ID")
async def read_artist(artist_id: UUID):
    """
    Retrieve a specific artist by their unique ID. This endpoint is public.
    """
    db_artist = await crud.get_artist(artist_id=artist_id)
    if db_artist is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Artist not found")
    return db_artist

@router.put("/{artist_id}", response_model=schemas.ArtistResponse, summary="Update an existing artist (Admin only)")
async def update_artist_api(artist_id: UUID, artist_update: schemas.ArtistUpdate, admin: User = Depends(is_admin)):
    """
    Updates an existing artist. Requires admin privileges.
    """
    db_artist = await crud.get_artist(artist_id=artist_id)
    if db_artist is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Artist not found")
    
    return await crud.update_artist(artist_id=artist_id, artist=artist_update)

@router.delete("/{artist_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete an artist (Admin only)")
async def delete_artist_api(artist_id: UUID, admin: User = Depends(is_admin)):
    """
    Deletes an artist. Requires admin privileges.
    """
    db_artist = await crud.get_artist(artist_id=artist_id)
    if db_artist is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Artist not found")
    
    await crud.delete_artist(artist_id=artist_id)
    return None

@router.get("/{artist_id}/music", response_model=List[schemas.MusicResponse], summary="Retrieve music by artist ID")
async def get_music_by_artist_api(artist_id: UUID, skip: int = Query(0, ge=0), limit: int = Query(100, ge=1)):
    """
    Retrieve a list of music tracks by a specific artist ID. This endpoint is public.
    """
    music_list = await crud.get_music_by_artist_id(artist_id=artist_id, skip=skip, limit=limit)
    response_list = []
    for music in music_list:
        response_list.append(await crud.enrich_music_response(music))
    return response_list

@router.get("/{artist_id}/albums", response_model=List[schemas.AlbumResponse], summary="Retrieve albums by artist ID")
async def get_albums_by_artist_api(artist_id: UUID, skip: int = Query(0, ge=0), limit: int = Query(100, ge=1)):
    """
    Retrieve a list of albums by a specific artist ID. This endpoint is public.
    """
    albums = await crud.get_albums_by_artist_id(artist_id=artist_id, skip=skip, limit=limit)
    response_list = []
    for album in albums:
        response_list.append(await crud.enrich_album_response(album))
    return response_list