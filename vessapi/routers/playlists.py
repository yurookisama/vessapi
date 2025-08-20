from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List
from uuid import UUID

from vessapi import crud, schemas, models
from vessapi.auth import get_current_active_user

router = APIRouter(
    prefix="/playlists",
    tags=["playlists"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=schemas.PlaylistResponse, status_code=status.HTTP_201_CREATED, summary="Create a new playlist", description="Creates a new playlist. Requires authentication.")
async def create_playlist_api(playlist: schemas.PlaylistCreate, current_user: models.User = Depends(get_current_active_user)):
    return await crud.create_playlist(playlist=playlist, owner_id=current_user.user_id)

@router.get("/", response_model=List[schemas.PlaylistResponse], summary="Retrieve accessible playlists", description="Retrieves a list of public playlists and playlists owned by the current user.")
async def read_playlists(skip: int = Query(0, ge=0, description="Number of items to skip"), limit: int = Query(100, ge=1, le=1000, description="Maximum number of items to return"), current_user: models.User = Depends(get_current_active_user)):
    return await crud.get_playlists(skip=skip, limit=limit, user_id=current_user.user_id)

@router.get("/{playlist_id}", response_model=schemas.PlaylistResponse, summary="Retrieve a single playlist by ID", description="Retrieves a specific playlist by its ID. Can only be accessed by the owner or if the playlist is public.")
async def read_playlist(playlist_id: UUID, current_user: models.User = Depends(get_current_active_user)):
    db_playlist = await crud.get_playlist(playlist_id=playlist_id, user_id=current_user.user_id)
    if db_playlist is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Playlist not found or you don't have permission to view it")
    return db_playlist

@router.put("/{playlist_id}", response_model=schemas.PlaylistResponse, summary="Update an existing playlist", description="Updates an existing playlist identified by its ID. Only the owner of the playlist can update it.")
async def update_playlist_api(playlist_id: UUID, playlist: schemas.PlaylistUpdate, current_user: models.User = Depends(get_current_active_user)):
    db_playlist = await crud.update_playlist(playlist_id=playlist_id, playlist=playlist, owner_id=current_user.user_id)
    if db_playlist is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Playlist not found or you don't have permission to update it")
    return db_playlist

@router.delete("/{playlist_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a playlist", description="Deletes a playlist identified by its ID. Only the owner of the playlist can delete it.")
async def delete_playlist_api(playlist_id: UUID, current_user: models.User = Depends(get_current_active_user)):
    db_playlist = await crud.delete_playlist(playlist_id=playlist_id, owner_id=current_user.user_id)
    if db_playlist is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Playlist not found or you don't have permission to delete it")
    return

@router.post("/{playlist_id}/music/{music_id}", response_model=schemas.PlaylistResponse, summary="Add music to a playlist", description="Adds a music track to a specific playlist. Only the owner of the playlist can modify it.")
async def add_music_to_playlist_api(playlist_id: UUID, music_id: UUID, current_user: models.User = Depends(get_current_active_user)):
    db_playlist = await crud.add_music_to_playlist(playlist_id=playlist_id, music_id=music_id, owner_id=current_user.user_id)
    if db_playlist is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Playlist or Music not found or you don't have permission to modify it")
    return db_playlist

@router.delete("/{playlist_id}/music/{music_id}", response_model=schemas.PlaylistResponse, summary="Remove music from a playlist", description="Removes a music track from a specific playlist. Only the owner of the playlist can modify it.")
async def remove_music_from_playlist_api(playlist_id: UUID, music_id: UUID, current_user: models.User = Depends(get_current_active_user)):
    db_playlist = await crud.remove_music_from_playlist(playlist_id=playlist_id, music_id=music_id, owner_id=current_user.user_id)
    if db_playlist is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Playlist or Music not found or you don't have permission to modify it")
    return db_playlist

@router.get("/{playlist_id}/music/", response_model=List[schemas.MusicResponse], summary="Retrieve music tracks in a playlist", description="Retrieves all music tracks within a specific playlist.")
async def get_music_in_playlist(playlist_id: UUID, current_user: models.User = Depends(get_current_active_user)):
    return await crud.get_music_in_playlist(playlist_id=playlist_id)
