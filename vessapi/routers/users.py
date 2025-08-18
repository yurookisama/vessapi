from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List
from uuid import UUID

from vessapi import crud, schemas, models
from vessapi.auth import get_current_active_user, is_admin

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED, summary="Create a new user", description="Registers a new user with the provided details.")
async def create_user_api(user: schemas.UserCreate):
    db_user = await crud.get_user_by_email(email=user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    return await crud.create_user(user=user)

@router.get("/me/", response_model=schemas.UserResponse, summary="Retrieve current user's profile", description="Retrieves the profile information of the currently authenticated user.")
async def read_users_me(current_user: models.User = Depends(get_current_active_user)):
    return current_user

@router.get("/", response_model=List[schemas.UserResponse], summary="Retrieve all users (Admin only)", description="Retrieves a list of all registered users. Requires admin privileges.", dependencies=[Depends(is_admin)])
async def read_users(skip: int = Query(0, ge=0, description="Number of items to skip"), limit: int = Query(100, ge=1, le=1000, description="Maximum number of items to return"), current_user: models.User = Depends(get_current_active_user)):
    return await crud.get_users(skip=skip, limit=limit)

@router.get("/{user_id}", response_model=schemas.UserResponse, summary="Retrieve a single user by ID", description="Retrieves a specific user using their unique ID.")
async def read_user(user_id: UUID, current_user: models.User = Depends(get_current_active_user)):
    db_user = await crud.get_user(user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user

@router.put("/{user_id}", response_model=schemas.UserResponse, summary="Update an existing user", description="Updates an existing user identified by their ID. Only the user themselves or an admin can update their profile.")
async def update_user_api(user_id: UUID, user: schemas.UserUpdate, current_user: models.User = Depends(get_current_active_user)):
    db_user = await crud.get_user(user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if str(db_user.user_id) != str(current_user.user_id) and current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don't have permission to update this user")
    updated_user = await crud.update_user(user_id=user_id, user=user)
    if updated_user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to update user")
    return updated_user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a user", description="Deletes a user identified by their ID. Only the user themselves or an admin can delete their account.")
async def delete_user_api(user_id: UUID, current_user: models.User = Depends(get_current_active_user)):
    db_user = await crud.get_user(user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if str(db_user.user_id) != str(current_user.user_id) and current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don't have permission to delete this user")
    deleted_user = await crud.delete_user(user_id=user_id)
    if deleted_user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to delete user")
    return
