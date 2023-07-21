from os import environ
from datetime import datetime
from threading import local

import asyncpg
import logging


logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


async def db_connect() -> asyncpg.Connection:
    conn = await asyncpg.connect(
        user=environ["POSTGRES_USER"],
        password=environ["POSTGRES_PASSWORD"],
        database=environ["POSTGRES_DB"],
        host=environ["URL_DB"]
    )
    return conn


async def locale_get(user_id: int) -> str:
    conn = await db_connect()
    locale = await conn.fetch(f"SELECT lang FROM users WHERE user_id='{user_id}'")
    await conn.close()
    match locale:
        case []:
            return ""
    return locale[0].get("lang")


async def new_user(user_id: int, lang: str) -> None:
    conn = await db_connect()
    await conn.execute("INSERT INTO users (user_id, lang, purchases, start_date) VALUES ($1, $2, $3, $4)", user_id, lang, 0, datetime.now())
    await conn.close()
    logger.info(f"New user in a database: {user_id}")


async def check_user(user_id: int) -> bool:
    conn = await db_connect()
    user = await conn.fetch(f"SELECT user_id FROM users WHERE user_id='{user_id}'")
    await conn.close()
    match user:
        case []:
            return False
    return True
