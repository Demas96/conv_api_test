from datetime import datetime, timedelta

from app.models.users import users_table, tokens_table
from app.db import database


async def get_user_by_name(name: str):
    query = users_table.select().where(users_table.c.name == name)
    return await database.fetch_one(query)


async def create_user_token(user_id: int):
    query = (
        tokens_table.insert()
        .values(expires=datetime.now() + timedelta(weeks=2), user_id=user_id)
        .returning(tokens_table.c.token, tokens_table.c.expires)
    )

    return await database.fetch_one(query)


async def create_user(user: str):
    query = users_table.insert().values(
        name=user
    )
    user_id = await database.execute(query)
    token = await create_user_token(user_id)

    return {"id": user_id, "token": token["token"]}
