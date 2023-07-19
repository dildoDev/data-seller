import logging


logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


async def locale_get(user_id: int) -> str:
    return "ru"


async def new_user(logger: logging.Logger, user_id: int) -> None:
    logger.info(f"New user in a database: {user_id}")
