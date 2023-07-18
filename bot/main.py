from pyrogram.client import Client
from pyrogram.types import Message
from os import environ

import logging
import uvloop


# Logs
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# Bot info constants
try:
    API_ID = int(environ["API_ID"])
    API_HASH = environ["API_HASH"]
    BOT_TOKEN = environ["BOT_TOKEN"]
except (KeyError, ValueError):
    logger.critical("Please recheck ENV variables!")
    raise


# Define a faster loop and bot
uvloop.install()
bot = Client("bot", API_ID, API_HASH, bot_token=BOT_TOKEN)


# !!! Bot events !!!

@bot.on_message()
async def hello(client: Client, message: Message):
    await client.send_message(message.chat.id, "Hello.")


# Run application
if __name__ == "__main__":
    try:
        bot.run()
        logger.debug("The bot was successfully started")
    except:
        logger.exception("Unexpected error")
        raise