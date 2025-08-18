from uuid import UUID, uuid4
import os
from mutagen import File as MutagenFile
from datetime import datetime

from vessapi import crud, schemas

SYSTEM_USER_ID = UUID('00000000-0000-0000-0000-000000000001') # Sabit sistem kullanıcısı ID'si

MUSIC_UPLOAD_DIRECTORY = "library/music"
ALBUM_IMAGE_DIRECTORY = "library/images/album_image"

async def process_music_upload_task(music_file_path: str, music_cover_image_url: str | None, current_user_id: UUID | None):
    try:
        audio = MutagenFile(music_file_path)
        
        title = audio.get('title', [os.path.basename(music_file_path).split('.')[0]])[0]
        
        artist_names = [a.strip() for a in audio.get('artist', ['Unknown Artist'])[0].split(',')] if audio.get('artist') else ['Unknown Artist']
        artist_ids = []
        for artist_name in artist_names:
            artist = await crud.get_artist_by_name(artist_name)
            if not artist:
                artist_create = schemas.ArtistCreate(name=artist_name)
                artist = await crud.create_artist(artist_create)
            artist_ids.append(artist.artist_id)

        duration = int(audio.info.length) if audio.info.length else 0
        genre = audio.get('genre', ['Unknown'])[0]
        
        publish_date_str = audio.get('date', [str(datetime.now().year)])[0]
        try:
            publish_date = datetime.strptime(publish_date_str, "%Y-%m-%d")
        except ValueError:
            try:
                publish_date = datetime.strptime(publish_date_str, "%Y")
            except ValueError:
                publish_date = datetime.now()

            album_title = audio.get('album', [None])[0]
            album_artist_name = audio.get('albumartist', [artist_names[0]])[0] if artist_names else 'Unknown Artist'
            album_artist_id = None
            album_cover_image_url = None

            if album_title and album_artist_name:
                album_artist_obj = await crud.get_artist_by_name(album_artist_name)
                if not album_artist_obj:
                    album_artist_create = schemas.ArtistCreate(name=album_artist_name)
                    album_artist_obj = await crud.create_artist(album_artist_create)
                album_artist_id = album_artist_obj.artist_id

                existing_album = await crud.get_album_by_title_and_artist_id(album_title, album_artist_id)
                if existing_album:
                    album_id = existing_album.album_id
                    album_cover_image_url = existing_album.cover_image_url
                else:
                    album_image_data = None
                    if hasattr(audio, 'pictures') and audio.pictures:
                        album_image_data = audio.pictures[0].data
                    elif hasattr(audio, 'tags') and 'APIC:' in audio.tags:
                        album_image_data = audio.tags['APIC:'].data
                    
                    if album_image_data:
                        album_cover_filename = f"{uuid4()}.png"
                        album_cover_path = os.path.join(ALBUM_IMAGE_DIRECTORY, album_cover_filename)
                        try:
                            with open(album_cover_path, "wb") as img_buffer:
                                img_buffer.write(album_image_data)
                            album_cover_image_url = f"/library/images/album_image/{album_cover_filename}"
                        except Exception as img_e:
                            print(f"Error extracting and saving album cover for '{album_title}': {img_e}")

                    new_album = schemas.AlbumCreate(
                        title=album_title,
                        artist_id=album_artist_id,
                        release_date=publish_date.date(),
                        cover_image_url=album_cover_image_url or music_cover_image_url or "",
                        genre=genre,
                        description=None
                    )
                    created_album = await crud.create_album(album=new_album, owner_id=current_user_id if current_user_id else SYSTEM_USER_ID)
                    album_id = created_album.album_id

        music_create = schemas.MusicCreate(
            title=title, 
            artist_ids=artist_ids, 
            duration=duration, 
            file_path=music_file_path, 
            genre=genre, 
            publish_date=publish_date,
            lyrics=audio.get('lyrics', [None])[0], 
            album_id=album_id, 
            cover_image_url=music_cover_image_url or album_cover_image_url
        )
        owner_id = current_user_id if current_user_id else SYSTEM_USER_ID
        await crud.create_music(music=music_create, owner_id=owner_id)
        print(f"File '{os.path.basename(music_file_path)}' processed and registered successfully.")
    except Exception as e:
        print(f"Error processing file '{os.path.basename(music_file_path)}': {e}")
