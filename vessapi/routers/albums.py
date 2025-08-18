from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from uuid import UUID
from datetime import date

from vessapi import crud, schemas, models
from vessapi.auth import get_current_active_user

router = APIRouter(
    prefix="/albums",
    tags=["albums"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=schemas.AlbumResponse, status_code=status.HTTP_201_CREATED, summary="Create a new album", description="Creates a new album with the provided details. Requires authentication.")
async def create_album_api(album: schemas.AlbumCreate, current_user: models.User = Depends(get_current_active_user)):
    return await crud.create_album(album=album, owner_id=current_user.user_id)

@router.get("/", response_model=List[schemas.AlbumResponse], summary="Retrieve all albums with optional filtering", description="Retrieves a list of all albums. Supports pagination and filtering by title, artist ID, genre, and release date.")
async def read_albums(
    skip: int = Query(0, ge=0, description="Number of items to skip"), 
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of items to return"), 
    title: Optional[str] = Query(None, description="Search by album title (case-insensitive)"),
    artist_id: Optional[UUID] = Query(None, description="Filter by artist ID"),
    genre: Optional[str] = Query(None, description="Filter by genre (case-insensitive)"),
    start_date: Optional[date] = Query(None, description="Filter by release date (start of range)"),
    end_date: Optional[date] = Query(None, description="Filter by release date (end of range)")
):
    albums = await crud.get_albums(
        skip=skip, 
        limit=limit, 
        title=title, 
        artist_id=artist_id, 
        genre=genre, 
        start_date=start_date, 
        end_date=end_date
    )
    albums_with_artist_names = []
    for album in albums:
        album_dict = album.model_dump()
        album_dict["num_tracks"] = len(album.music_ids)
        artist = await crud.get_artist(album.artist_id)
        if artist:
            album_dict["artist_name"] = artist.name
        albums_with_artist_names.append(schemas.AlbumResponse(**album_dict))
    return albums_with_artist_names

@router.get("/{album_id}", response_model=schemas.AlbumResponse, summary="Retrieve a single album by ID", description="Retrieves a specific album using its unique ID.")
async def read_album(album_id: UUID):
    db_album = await crud.get_album(album_id=album_id)
    if db_album is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Album not found")
    
    album_dict = db_album.model_dump()
    album_dict["num_tracks"] = len(db_album.music_ids)
    artist = await crud.get_artist(db_album.artist_id)
    if artist:
        album_dict["artist_name"] = artist.name
    return schemas.AlbumResponse(**album_dict)

@router.put("/{album_id}", response_model=schemas.AlbumResponse, summary="Update an existing album", description="Updates an existing album identified by its ID. Only the owner of the album can update it.")
async def update_album_api(album_id: UUID, album: schemas.AlbumUpdate, current_user: models.User = Depends(get_current_active_user)):
    db_album = await crud.update_album(album_id=album_id, album=album, owner_id=current_user.user_id)
    if db_album is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Album not found or you don't have permission to update it")
    return db_album

@router.delete("/{album_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete an album", description="Deletes an album identified by its ID. Only the owner of the album can delete it.")
async def delete_album_api(album_id: UUID, current_user: models.User = Depends(get_current_active_user)):
    db_album = await crud.delete_album(album_id=album_id, owner_id=current_user.user_id)
    if db_album is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Album not found or you don't have permission to delete it")
    return
