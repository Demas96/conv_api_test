# Converter .wav to .mp3 

Данный API имеет возможность пользователю зарегистрироваться и отправить файл расширения .wav для конвертации в .mp3

## Основной стек

* FastAPI
* PostgreSQL
* ffmpeg

## Запуск

Скачать репозиторий и выполнить команду

    docker-compose up

# REST API
 Автоматическую документацию можно посмотреть по ссылке  http://127.0.0.1:8000/docs

REST API описан ниже

## Регистрация

### Request

`POST /sign-up/`

    curl -X 'POST' \
    'http://127.0.0.1:8000/sign-up?user={user_name}' \
    -H 'accept: application/json' \
    -d ''


### Response

    {
        "id": {user_id},
        "token": "{user_token}"
    }

## Загрузить и конвертировать файл

### Request

`POST /uploadfile/`

    curl -X 'POST' \
    'http://127.0.0.1:8000/uploadfile/?user_id={user_id}&token={user_token}' \
    -H 'accept: application/json' \
    -H 'Content-Type: multipart/form-data' \
    -F 'file={file_path};type=audio/wav'

### Response

    {
        "link": "http://127.0.0.1:8000/record?id={audio_token}&user={user_id}"
    }

## Скачать .mp3 файл

### Request

`GET /record/`

    curl -X 'GET' \
    'http://127.0.0.1:8000/record?id={audio_token}&user={user_id}' \
    -H 'accept: application/json'