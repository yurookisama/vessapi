from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from uuid import UUID

from vessapi import crud, schemas
from vessapi.models import User, UserRole
from vessapi.auth import get_current_active_user, has_role

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# Admin role dependency
is_admin = has_role([UserRole.ADMIN])

@router.post("/", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED, summary="Create a new user")
async def create_user(user: schemas.UserCreate):
    """
    Create a new user. This endpoint is public.
    """
    db_user = await crud.get_user_by_username(username=user.username)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
    return await crud.create_user(user=user)

@router.get("/me", response_model=schemas.UserResponse, summary="Get current user's details")
async def read_current_user(current_user: User = Depends(get_current_active_user)):
    """
    Get details for the currently authenticated user.
    """
    return current_user

@router.put("/me", response_model=schemas.UserResponse, summary="Update current user's details")
async def update_current_user(user_update: schemas.UserUpdate, current_user: User = Depends(get_current_active_user)):
    """
    Update details for the currently authenticated user.
    """
    return await crud.update_user(user_id=current_user.user_id, user=user_update)

@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT, summary="Delete current user's account")
async def delete_current_user(current_user: User = Depends(get_current_active_user)):
    """
    Delete the account of the currently authenticated user.
    """
    await crud.delete_user(user_id=current_user.user_id)
    return None

# --- Admin Routes ---

@router.get("/", response_model=List[schemas.UserResponse], summary="List all users (Admin only)")
async def read_users(skip: int = 0, limit: int = 100, admin: User = Depends(is_admin)):
    """
    Retrieve a list of all users. Requires admin privileges.
    """
    users = await crud.get_users(skip=skip, limit=limit)
    return users

@router.get("/{user_id}", response_model=schemas.UserResponse, summary="Get user by ID (Admin only)")
async def read_user_by_id(user_id: UUID, admin: User = Depends(is_admin)):
    """
    Retrieve a single user by their ID. Requires admin privileges.
    """
    db_user = await crud.get_user(user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a user by ID (Admin only)")
async def delete_user_by_id(user_id: UUID, admin: User = Depends(is_admin)):
    """
    Delete a specific user by their ID. Requires admin privileges.
    """
    db_user = await crud.get_user(user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    await crud.delete_user(user_id=user_id)
    return None