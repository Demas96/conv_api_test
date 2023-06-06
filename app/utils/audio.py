import os
import shutil

from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError
from urllib.parse import urlparse, urlunparse, urlencode
from fastapi import HTTPException
from fastapi.responses import FileResponse

from app.db import database
from app.models.users import audio_table, users_table, tokens_table


def build_url(base_url, path, args_dict):
    url_parts = list(urlparse(base_url))
    url_parts[2] = path
    url_parts[4] = urlencode(args_dict)
    return urlunparse(url_parts)


async def check_user(user_id, token):
    query = users_table.join(tokens_table).select().where(users_table.c.id == user_id)
    user = await database.fetch_one(query)
    if user is None:
        raise HTTPException(status_code=400, detail=f"User {user_id} does not exist")
    if str(user.token) != token:
        raise HTTPException(status_code=400, detail=f"Wrong token for user {user_id}")
    return user


async def download_audio(user_id, token):
    query = audio_table.select().where(audio_table.c.token == token, audio_table.c.user_id == user_id)
    data = await database.fetch_all(query)
    if not data:
        raise HTTPException(status_code=400, detail=f"Invalid link")
    return FileResponse(
        path=f'{os.path.join(data[0]["path"], str(data[0]["token"]) + ".mp3")}',
        filename=f'{data[0]["name"]}.mp3',
        media_type='multipart/form-data'
    )


async def add_audio(file, user_id, token, request):
    if not file.filename:
        raise HTTPException(status_code=400, detail=f"No File")
    db_user = await check_user(user_id=user_id, token=token)
    with open(os.path.join(os.getcwd(), 'app', 'static', 'mp3', file.filename), "wb") as wf:
        shutil.copyfileobj(file.file, wf)
        file.file.close()
    query = audio_table.insert().values(
        name=f'{os.path.splitext(file.filename)[0]}',
        path=f"{os.path.join(os.getcwd(), 'app', 'static', 'mp3')}",
        user_id=db_user.id
    ).returning(audio_table.c.token, audio_table.c.user_id)
    data = await database.fetch_all(query)
    try:
        AudioSegment.from_wav(f"{os.path.join(os.getcwd(), 'app', 'static', 'mp3', file.filename)}")\
            .export(f"{os.path.join(os.getcwd(), 'app', 'static', 'mp3', str(data[0]['token']) + '.mp3')}",
                    format="mp3")
    except CouldntDecodeError:
        os.remove(f"{os.path.join(os.getcwd(), 'app', 'static', 'mp3', file.filename)}")
        d = audio_table.delete().where(audio_table.c.token == str(data[0]['token']))
        await database.execute(d)
        raise HTTPException(status_code=400, detail=f"Invalid format file")
    os.remove(f"{os.path.join(os.getcwd(), 'app', 'static', 'mp3', file.filename)}")
    args = {'id': f'{data[0]["token"]}', 'user': f'{data[0]["user_id"]}'}
    url_download = build_url(str(request.url), 'record', args)
    return {'link': url_download}
