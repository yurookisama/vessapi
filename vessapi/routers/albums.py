from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from uuid import UUID
from datetime import date

from vessapi import crud, schemas, models
from vessapi.auth import get_current_active_user, has_role
from vessapi.models import UserRole, User

router = APIRouter(
    prefix="/albums",
    tags=["Albums"],
    responses={404: {"description": "Not found"}},
)

# Admin role dependency
is_admin = has_role([UserRole.ADMIN])

@router.post("/", response_model=schemas.AlbumResponse, status_code=status.HTTP_201_CREATED, summary="Create new album (Admin only)")
async def create_album_api(album: schemas.AlbumCreate, admin: User = Depends(is_admin)):
    """
    Create a new album entry. Requires admin privileges.
    The owner_id will be set to the admin's user_id.
    """
    return await crud.create_album(album=album, owner_id=admin.user_id)

@router.get("/", response_model=List[schemas.AlbumResponse], summary="Retrieve all albums")
async def read_albums(
    skip: int = Query(0, ge=0), 
    limit: int = Query(100, ge=1), 
    title: Optional[str] = Query(None),
    artist_id: Optional[UUID] = Query(None),
    genre: Optional[str] = Query(None)
):
    """
    Retrieve a list of all albums. This endpoint is public.
    Supports pagination and filtering.
    """
    albums = await crud.get_albums(
        skip=skip, 
        limit=limit, 
        title=title, 
        artist_id=artist_id, 
        genre=genre
    )
    # This part can be optimized
    response_list = []
    for album in albums:
        response_list.append(await crud.enrich_album_response(album))
    return response_list

@router.get("/{album_id}", response_model=schemas.AlbumResponse, summary="Retrieve a single album by ID")
async def read_album(album_id: UUID):
    """
    Retrieve a specific album by its unique ID. This endpoint is public.
    """
    db_album = await crud.get_album(album_id=album_id)
    if db_album is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Album not found")
    return await crud.enrich_album_response(db_album)

@router.put("/{album_id}", response_model=schemas.AlbumResponse, summary="Update an existing album (Admin only)")
async def update_album_api(album_id: UUID, album_update: schemas.AlbumUpdate, admin: User = Depends(is_admin)):
    """
    Updates an existing album. Requires admin privileges.
    """
    db_album = await crud.get_album(album_id=album_id)
    if db_album is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Album not found")
    
    updated_album = await crud.update_album(album_id=album_id, album=album_update, owner_id=admin.user_id, is_admin=True)
    return await crud.enrich_album_response(updated_album)

@router.delete("/{album_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete an album (Admin only)")
async def delete_album_api(album_id: UUID, admin: User = Depends(is_admin)):
    """
    Deletes an album. Requires admin privileges.
    """
    db_album = await crud.get_album(album_id=album_id)
    if db_album is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Album not found")
    
    await crud.delete_album(album_id=album_id, owner_id=admin.user_id, is_admin=True)
    return None