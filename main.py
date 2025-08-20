import os
from fastapi import FastAPI, Depends, HTTPException, status, Request, Form
from datetime import timedelta
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordRequestForm

from vessapi import crud, schemas, models
from vessapi.database import init_db
from vessapi.auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, Token
from vessapi.routers import music, albums, users, playlists, artists, web

app = FastAPI(
    title="VessAPI",
    description="API service for music applications to sync music, albums, users, and playlists.",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_event():
    await init_db()
    os.makedirs("library/music", exist_ok=True)
    os.makedirs("library/images/album_image", exist_ok=True)
    os.makedirs("library/images/music_image", exist_ok=True)
    os.makedirs("library/images/user_image", exist_ok=True)
    os.makedirs("library/images/artist_image", exist_ok=True)
    port = os.environ.get("PORT", "8000")
    print(f"VessAPI is running on port {port}")

# CORS Middleware
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
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
