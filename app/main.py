import sqlalchemy

from fastapi import HTTPException, Request, FastAPI, UploadFile

from app.db import DATABASE_URL, database
from app.utils.users import get_user_by_name, create_user
from app.utils.audio import add_audio, download_audio

app = FastAPI()

engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/record")
async def download(id: str, user: int):
    return await download_audio(user, id)


@app.post("/sign-up/")
async def create(user: str):
    db_user = await get_user_by_name(name=user)
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")
    return await create_user(user=user)


@app.post("/uploadfile/")
async def upload_file(file: UploadFile, user_id: int, token: str, request: Request):
    return await add_audio(file=file, user_id=user_id, token=token, request=request)
