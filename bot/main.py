from pyrogram.client import Client
from pyrogram.types import Message
from pyrogram import filters

from db_interface import *
from os import environ
from json import load

import logging
import uvloop


# Logs
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# Localization
async def locale_load(user_id: int) -> dict:
    try:
        with open("localization.json", 'r') as file:
            locale = await locale_get(user_id)
            localization = load(file)[locale]
        return localization
    
    except FileNotFoundError:
        logger.critical("Please check your localization file!")
        raise
    

# Bot info constants
try:
    API_ID = int(environ["API_ID"])
    API_HASH = environ["API_HASH"]
    BOT_TOKEN = environ["BOT_TOKEN"]
    logger.debug("ENV variables was successfully loaded")

except (KeyError, ValueError):
    logger.critical("Please recheck ENV variables!")
    raise


# Define a faster loop and bot
uvloop.install()
bot = Client("bot", API_ID, API_HASH, bot_token=BOT_TOKEN)


# !!! Bot events !!!

@bot.on_message(filters=filters.command(["start", "help"]))
async def start(client: Client, message: Message) -> None:
    localization = await locale_load(message.from_user.id)
    await client.send_sticker(message.chat.id, "Static/sticker.webp")
    await client.send_message(message.chat.id, localization["hello-message"])
    await new_user(logger, message.from_user.id)
    logger.info(f"Greeting message was sent to @{message.from_user.username}")


# Run application
if __name__ == "__main__":
    try:
        logger.debug("Starting bot...")
        bot.run()
        
    except:
        logger.exception("Unexpected error")
        raise
