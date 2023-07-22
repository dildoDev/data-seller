from os import environ
from datetime import datetime
from datetime import date
from threading import local
import time

import asyncpg
import logging

from pyrogram.raw.types import reaction_custom_emoji


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


async def purchases_get(user_id: int) -> int:
    conn = await db_connect()
    purchases = await conn.fetch(f"SELECT purchases FROM users WHERE user_id='{user_id}'")
    await conn.close()
    match purchases:
        case []:
            return 0
    return purchases[0].get("purchases")


async def start_time_get(user_id: int) -> str:
    conn = await db_connect()
    timestamp = await conn.fetch(f"SELECT start_date FROM users WHERE user_id='{user_id}'")
    await conn.close()
    match timestamp:
        case []:
            return str(datetime.now().date())
    return timestamp[0].get("start_date").date()


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
