import os

from dotenv import load_dotenv


load_dotenv(".env")

HOST_DB = os.environ.get("HOST_DB")
PORT_DB = os.environ.get("PORT_DB")
NAME_DB = os.environ.get("NAME_DB")
USER_DB = os.environ.get("USER_DB")
PASSWORD_DB = os.environ.get("PASSWORD_DB")