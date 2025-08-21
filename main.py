import os
from fastapi import FastAPI, Depends, HTTPException, status, Request, Form
from datetime import timedelta
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordRequestForm

from vessapi import crud, schemas, models
from vessapi.database import init_db
from vessapi.auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, Token
from vessapi.config import settings
from vessapi.routers import music, albums, users, playlists, artists, web

app = FastAPI(
    title="VessAPI",
    description="API service for music applications to sync music, albums, users, and playlists.",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_event():
    await init_db()
    settings.create_directories()
    print(f"VessAPI is running on {settings.server.host}:{settings.server.port}")
    print(f"Database: {settings.database.url}/{settings.database.name}")
    print(f"Debug mode: {settings.server.debug}")

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.server.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/library", StaticFiles(directory="library"), name="library")

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await crud.get_user_by_username(username=form_data.username)
    if not user or not crud.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
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



# Include routers
app.include_router(web.router)
app.include_router(music.router, prefix="/v1")
app.include_router(albums.router, prefix="/v1")
app.include_router(users.router, prefix="/v1")
app.include_router(playlists.router, prefix="/v1")
app.include_router(artists.router, prefix="/v1")

@app.post("/admin/reset-users", summary="Delete all users from the database (admin only)")
async def reset_users():
    deleted = await models.User.delete_all({})
    return {"message": f"All users deleted. Count: {deleted.deleted_count}"}
