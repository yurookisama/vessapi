from fastapi import FastAPI, Depends, HTTPException, status, Request, Form
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from datetime import timedelta
import os

from vessapi import crud, schemas, models
from vessapi.database import init_db
from vessapi.auth import (create_access_token, 
                  ACCESS_TOKEN_EXPIRE_MINUTES, Token)
from vessapi.routers import music, albums, users, playlists, artists, web

app = FastAPI(
    title="VessAPI",
    description="API service for music applications to sync music, albums, users, and playlists.",
    version="1.0.0"
)

# Custom Exceptions
class NotFoundException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class BadRequestException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

class ForbiddenException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)

# Exception Handlers
@app.exception_handler(NotFoundException)
async def not_found_exception_handler(request: Request, exc: NotFoundException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )

@app.exception_handler(BadRequestException)
async def bad_request_exception_handler(request: Request, exc: BadRequestException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )

@app.exception_handler(ForbiddenException)
async def forbidden_exception_handler(request: Request, exc: ForbiddenException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/library", StaticFiles(directory="library"), name="library")

@app.on_event("startup")
async def on_startup():
    await init_db()
    os.makedirs("library/music", exist_ok=True)
    os.makedirs("library/images/album_image", exist_ok=True)
    os.makedirs("library/images/music_image", exist_ok=True)
    os.makedirs("library/images/user_image", exist_ok=True)
    os.makedirs("library/images/artist_image", exist_ok=True)

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await crud.get_user_by_email(email=form_data.username)
    if not user or not crud.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/health", summary="Check API health and database connection")
async def health_check():
    try:
        await models.User.count()
        db_status = "connected"
    except Exception:
        db_status = "disconnected"
    return {"status": "ok", "database": db_status}


app.include_router(web.router)
app.include_router(music.router, prefix="/v1")
app.include_router(albums.router, prefix="/v1")
app.include_router(users.router, prefix="/v1")
app.include_router(playlists.router, prefix="/v1")
app.include_router(artists.router, prefix="/v1")