from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from uuid import UUID
from datetime import date

from vessapi import crud, schemas, models
from vessapi.auth import get_current_active_user, has_role
from vessapi.models import UserRole, User

router = APIRouter(
    prefix="/songs",
    tags=["Songs"],
    responses={404: {"description": "Not found"}},
)

# Admin role dependency
is_admin = has_role([UserRole.ADMIN])

@router.post("/", response_model=schemas.MusicResponse, status_code=status.HTTP_201_CREATED, summary="Create new music (Admin only)")
async def create_music_api(music: schemas.MusicCreate, admin: User = Depends(is_admin)):
    """
    Create a new music entry. Requires admin privileges.
    The owner_id will be set to the admin's user_id.
    """
    return await crud.create_music(music=music, owner_id=admin.user_id)

@router.get("/", response_model=List[schemas.MusicResponse], summary="Retrieve all music tracks")
async def read_music_all(
    skip: int = Query(0, ge=0), 
    limit: int = Query(100, ge=1), 
    title: Optional[str] = Query(None),
    artist_id: Optional[UUID] = Query(None),
    genre: Optional[str] = Query(None)
):
    """
    Retrieve a list of all music tracks. This endpoint is public.
    Supports pagination and filtering.
    """
    music_list = await crud.get_music_all(
        skip=skip, 
        limit=limit, 
        title=title, 
        artist_ids=[artist_id] if artist_id else None, 
        genre=genre
    )
    # This part can be optimized, but following existing pattern for now
    response_list = []
    for music in music_list:
        response_list.append(await crud.enrich_music_response(music))
    return response_list

@router.get("/{music_id}", response_model=schemas.MusicResponse, summary="Retrieve a single music track by ID")
async def read_music(music_id: UUID):
    """
    Retrieve a specific music track by its unique ID. This endpoint is public.
    """
    db_music = await crud.get_music(music_id=music_id)
    if db_music is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Music not found")
    return await crud.enrich_music_response(db_music)

@router.put("/{music_id}", response_model=schemas.MusicResponse, summary="Update an existing music track (Admin only)")
async def update_music_api(music_id: UUID, music_update: schemas.MusicUpdate, admin: User = Depends(is_admin)):
    """
    Updates an existing music track. Requires admin privileges.
    """
    db_music = await crud.get_music(music_id=music_id)
    if db_music is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Music not found")
    
    updated_music = await crud.update_music(music_id=music_id, music=music_update, owner_id=admin.user_id, is_admin=True)
    return await crud.enrich_music_response(updated_music)

@router.delete("/{music_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a music track (Admin only)")
async def delete_music_api(music_id: UUID, admin: User = Depends(is_admin)):
    """
    Deletes a music track. Requires admin privileges.
    """
    db_music = await crud.get_music(music_id=music_id)
    if db_music is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Music not found")
    
    await crud.delete_music(music_id=music_id, owner_id=admin.user_id, is_admin=True)
    return None

@router.get("/{music_id}/stream", summary="Stream a music track")
async def stream_music(music_id: UUID):
    """
    Stream a music track by its ID. This endpoint is public.
    """
    from fastapi.responses import FileResponse
    import os
    
    db_music = await crud.get_music(music_id=music_id)
    if db_music is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Music not found")
    
    # Check if file exists
    if not os.path.exists(db_music.file_path):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Music file not found")
    
    return FileResponse(
        path=db_music.file_path,
        media_type="audio/mpeg",
        filename=f"{db_music.title}.mp3"
    )