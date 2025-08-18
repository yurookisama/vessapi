from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from uuid import UUID
from datetime import date

from vessapi import crud, schemas, models
from vessapi.auth import get_current_active_user

router = APIRouter(
    prefix="/music",
    tags=["music"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=schemas.MusicResponse, status_code=status.HTTP_201_CREATED, summary="Create a new music track", description="Creates a new music track with the provided details. Requires authentication.")
async def create_music_api(music: schemas.MusicCreate, current_user: models.User = Depends(get_current_active_user)):
    return await crud.create_music(music=music, owner_id=current_user.user_id)

@router.get("/", response_model=List[schemas.MusicResponse], summary="Retrieve all music tracks with optional filtering", description="Retrieves a list of all music tracks. Supports pagination and filtering by title, artist ID, genre, duration, and publish date.")
async def read_music_all(
    skip: int = Query(0, ge=0, description="Number of items to skip"), 
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of items to return"), 
    title: Optional[str] = Query(None, description="Search by music title (case-insensitive)"),
    artist_id: Optional[UUID] = Query(None, description="Filter by artist ID"),
    genre: Optional[str] = Query(None, description="Filter by genre (case-insensitive)"),
    min_duration: Optional[int] = Query(None, ge=0, description="Filter by minimum duration in seconds"),
    max_duration: Optional[int] = Query(None, ge=0, description="Filter by maximum duration in seconds"),
    start_date: Optional[date] = Query(None, description="Filter by publish date (start of range)"),
    end_date: Optional[date] = Query(None, description="Filter by publish date (end of range)")
):
    music_list = await crud.get_music_all(
        skip=skip, 
        limit=limit, 
        title=title, 
        artist_ids=[artist_id] if artist_id else None, 
        genre=genre, 
        min_duration=min_duration, 
        max_duration=max_duration, 
        start_date=start_date, 
        end_date=end_date
    )
    music_with_artist_names = []
    for music_item in music_list:
        music_dict = music_item.model_dump()
        display_artists = []
        for art_id in music_item.artist_ids:
            artist = await crud.get_artist(art_id)
            if artist:
                display_artists.append({"id": artist.artist_id, "name": artist.name})
        music_dict["artist_names"] = display_artists
        music_with_artist_names.append(schemas.MusicResponse(**music_dict))
    return music_with_artist_names

@router.get("/{music_id}", response_model=schemas.MusicResponse, summary="Retrieve a single music track by ID", description="Retrieves a specific music track using its unique ID.")
async def read_music(music_id: UUID):
    db_music = await crud.get_music(music_id=music_id)
    if db_music is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Music not found")
    
    music_dict = db_music.model_dump()
    display_artists = []
    for art_id in db_music.artist_ids:
        artist = await crud.get_artist(art_id)
        if artist:
            display_artists.append({"id": artist.artist_id, "name": artist.name})
    music_dict["display_artists"] = display_artists
    return schemas.MusicResponse(**music_dict)

@router.put("/{music_id}", response_model=schemas.MusicResponse, summary="Update an existing music track", description="Updates an existing music track identified by its ID. Only the owner of the track can update it.")
async def update_music_api(music_id: UUID, music: schemas.MusicUpdate, current_user: models.User = Depends(get_current_active_user)):
    db_music = await crud.update_music(music_id=music_id, music=music, owner_id=current_user.user_id)
    if db_music is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Music not found or you don't have permission to update it")
    return db_music

@router.delete("/{music_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a music track", description="Deletes a music track identified by its ID. Only the owner of the track can delete it.")
async def delete_music_api(music_id: UUID, current_user: models.User = Depends(get_current_active_user)):
    db_music = await crud.delete_music(music_id=music_id, owner_id=current_user.user_id)
    if db_music is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Music not found or you don't have permission to delete it")
    return
