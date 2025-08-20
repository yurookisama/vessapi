from fastapi import APIRouter, Depends, Request, Form, File, UploadFile, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import List, Optional
from uuid import UUID
import shutil
import os
import asyncio


from vessapi import crud, schemas, models
from vessapi.auth import get_current_active_user
from vessapi.services import process_music_upload_task, SYSTEM_USER_ID

router = APIRouter(
    tags=["web"],
    responses={404: {"description": "Not found"}},
)

templates = Jinja2Templates(directory="templates")

MUSIC_UPLOAD_DIRECTORY = "library/music"
ALBUM_IMAGE_DIRECTORY = "library/images/album_image"
MUSIC_IMAGE_DIRECTORY = "library/images/music_image"

@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.post("/register", response_class=HTMLResponse)
async def register_user(request: Request, username: str = Form(...), password: str = Form(...), full_name: str = Form(None)):
    db_user = await crud.get_user_by_username(username=username)
    if db_user:
        return templates.TemplateResponse("index.html", {"request": request, "message": "Username already registered", "error": True})
    
    user_create = schemas.UserCreate(username=username, password=password, full_name=full_name)
    await crud.create_user(user=user_create)
    return templates.TemplateResponse("index.html", {"request": request, "message": "User registered successfully!", "error": False})

@router.post("/upload-music", response_class=HTMLResponse)
async def upload_music(request: Request, music_files: List[UploadFile] = File(...), cover_image: Optional[UploadFile] = File(None)):
    messages = []
    errors = []
    music_cover_image_url = None

    if cover_image and cover_image.filename:
        music_cover_image_path = os.path.join(MUSIC_IMAGE_DIRECTORY, cover_image.filename)
        try:
            with open(music_cover_image_path, "wb") as buffer:
                shutil.copyfileobj(cover_image.file, buffer)
            music_cover_image_url = f"/library/images/music_image/{cover_image.filename}"
            messages.append(f"Music cover image '{cover_image.filename}' uploaded successfully.")
        except Exception as e:
            errors.append(f"Error uploading music cover image '{cover_image.filename}': {e}")
        finally:
            cover_image.file.close()

    for music_file in music_files:
        file_location = os.path.join(MUSIC_UPLOAD_DIRECTORY, music_file.filename)
        try:
            with open(file_location, "wb") as buffer:
                shutil.copyfileobj(music_file.file, buffer)
            asyncio.create_task(process_music_upload_task(file_location, music_cover_image_url, SYSTEM_USER_ID))
            messages.append(f"File '{music_file.filename}' upload initiated. Processing in background.")
        except Exception as e:
            errors.append(f"Error saving file '{music_file.filename}': {e}")
        finally:
            music_file.file.close()
    
    return templates.TemplateResponse("index.html", {"request": request, "messages": messages, "errors": errors})

@router.post("/upload-album-cover", response_class=HTMLResponse)
async def upload_album_cover(request: Request, album_id: UUID = Form(...), cover_image: UploadFile = File(...)):
    album = await crud.get_album(album_id)
    if not album:
        raise HTTPException(status_code=404, detail="Album not found")

    file_location = os.path.join(ALBUM_IMAGE_DIRECTORY, cover_image.filename)
    try:
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(cover_image.file, buffer)
        
        album_update = schemas.AlbumUpdate(cover_image_url=f"/library/images/album_image/{cover_image.filename}")
        await crud.update_album(album_id, album_update, SYSTEM_USER_ID)
        return templates.TemplateResponse("index.html", {"request": request, "message": f"Album cover for '{album.title}' updated successfully!", "error": False})
    except Exception as e:
        return templates.TemplateResponse("index.html", {"request": request, "message": f"Error uploading album cover: {e}", "error": True})
    finally:
        cover_image.file.close()

@router.get("/music_page", response_class=HTMLResponse)
async def music_page(request: Request, skip: int = 0, limit: int = 10, q: Optional[str] = None, genre: Optional[str] = None):
    all_music = await crud.get_music_all()
    filtered_music = []
    for music in all_music:
        match = True
        if q and q.lower() not in music.title.lower() and not any(q.lower() in artist.name.lower() for artist_id in music.artist_ids for artist in [await crud.get_artist(artist_id)] if artist):
            match = False
        if genre and music.genre and genre.lower() != music.genre.lower():
            match = False
        if match:
            filtered_music.append(music)
    
    total_music = len(filtered_music)
    paginated_music = filtered_music[skip:skip + limit]

    music_response_list = []
    for music_item in paginated_music:
        music_dict = music_item.model_dump()
        display_artists = []
        for artist_id in music_item.artist_ids:
            artist = await crud.get_artist(artist_id)
            if artist:
                display_artists.append(artist.name)
        music_dict["artist_names"] = display_artists
        music_response_list.append(schemas.MusicResponse(**music_dict))

    return templates.TemplateResponse("music.html", {"request": request, "music": music_response_list, "skip": skip, "limit": limit, "total": total_music, "q": q, "genre": genre})

@router.get("/albums_page", response_class=HTMLResponse)
async def albums_page(request: Request, skip: int = 0, limit: int = 10, q: Optional[str] = None, artist_name: Optional[str] = None):
    albums = await crud.get_albums(skip=skip, limit=limit)
    albums_data = []
    for album in albums:
        album_dict = album.model_dump()
        album_dict["num_tracks"] = len(album.music_ids)
        artist = await crud.get_artist(album.artist_id)
        if artist:
            album_dict["artist_name"] = artist.name
        albums_data.append(schemas.AlbumResponse(**album_dict))
    
    filtered_albums = []
    for album in albums_data:
        match = True
        if q and q.lower() not in album.title.lower() and (album.artist_name and q.lower() not in album.artist_name.lower()):
            match = False
        if artist_name and album.artist_name and artist_name.lower() != album.artist_name.lower():
            match = False
        if match:
            filtered_albums.append(album)

    total_albums = len(filtered_albums)
    paginated_albums = filtered_albums[skip:skip + limit]

    return templates.TemplateResponse("albums.html", {"request": request, "albums": paginated_albums, "skip": skip, "limit": limit, "total": total_albums, "q": q, "artist": artist_name})

@router.get("/artists_page/{artist_id}", response_class=HTMLResponse)
async def artist_page(request: Request, artist_id: UUID):
    artist = await crud.get_artist(artist_id)
    if not artist:
        raise HTTPException(status_code=404, detail="Artist not found")
    
    music_by_artist = await crud.get_music_by_artist_id(artist_id)
    albums_by_artist = await crud.get_albums_by_artist_id(artist_id)

    for music_item in music_by_artist:
        music_item.artist_names = []
        for art_id in music_item.artist_ids:
            art = await crud.get_artist(art_id)
            if art:
                music_item.artist_names.append(art.name)

    albums_with_artist_names = []
    for album in albums_by_artist:
        album_dict = album.model_dump()
        album_dict["num_tracks"] = len(album.music_ids)
        art = await crud.get_artist(album.artist_id)
        if art:
            album_dict["artist_name"] = art.name
        albums_with_artist_names.append(schemas.AlbumResponse(**album_dict))

    return templates.TemplateResponse("artist.html", {"request": request, "artist": artist, "music": music_by_artist, "albums": albums_with_artist_names})


