from typing import AsyncIterable
from pyrogram.types import CallbackQuery, Message, User
from pyrogram.client import Client
from pyrogram import filters

from tools import lang_detection
from tools import db_interface
from tools.inline_kb import *
from os import environ
from json import load

import logging
import uvloop


# Logs

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# Normalize admins

def normalize_admins(admins: dict[str, str]) -> str:
    output = ""
    for username,position in admins.items():
        output += f"@{' - '.join(filter(lambda x: x, [username, position]))}\n"
    return output


# Localization

async def locale_load(from_user: User) -> dict[str, str]:
    try:
        with open("localization.json", 'r') as file:
            locale = await db_interface.locale_get(from_user.id)
            match locale:
                case "":
                    locale = lang_detection.detect(from_user.phone_number)
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


# Custom filters

def callback_data_filter(data: str) -> filters.Filter:
    async def func(flt, _, query):
        return flt.data == query.data or query.data.startswith(flt.data)
    return filters.create(func, data=data)


# !!! Bot events !!!


# Account callback

@bot.on_callback_query(filters=callback_data_filter("show_account"))
async def account(_, callback_query: CallbackQuery) -> None:
    localization = await locale_load(callback_query.from_user)
    lang = await db_interface.locale_get(callback_query.from_user.id)
    purchases = await db_interface.purchases_get(callback_query.from_user.id)
    start_time = await db_interface.start_time_get(callback_query.from_user.id)
    
    await callback_query.edit_message_text(
        localization["account-message"].format(
            username=callback_query.from_user.username,
            lang=lang,
            purchases=purchases,
            time=start_time),
        reply_markup=account_kb(localization)
    )
    logger.info(f"User @{callback_query.from_user.username} in account section")


# Settings callback

@bot.on_callback_query(filters=callback_data_filter("show_settings"))
async def settings(_, callback_query: CallbackQuery) -> None:
    localization = await locale_load(callback_query.from_user)
    await callback_query.edit_message_text(
        localization["settings-message"],
        reply_markup=settings_kb(localization)
    )
    logger.info(f"User @{callback_query.from_user.username} in settings section")


# Language settings callback

@bot.on_callback_query(filters=callback_data_filter("settings_lang"))
async def language(_, callback_query: CallbackQuery) -> None:
    localization = await locale_load(callback_query.from_user)
    await callback_query.edit_message_text(
        localization["lang-message"],
        reply_markup=lang_kb(localization)
    )
    logger.info(f"User @{callback_query.from_user.username} in language settings section")


# Set language callback

@bot.on_callback_query(filters=callback_data_filter("set_lang"))
async def set_lang(_, callback_query: CallbackQuery) -> None:
    lang = str(callback_query.data).split("_")[-1]
    await db_interface.change_lang(callback_query.from_user.id, lang)
    localization = await locale_load(callback_query.from_user)
    await callback_query.edit_message_text(
        localization["settings-message"],
        reply_markup=settings_kb(localization)
    )
    logger.info(f"User @{callback_query.from_user.username} in settings section")


# Support callback

@bot.on_callback_query(filters=callback_data_filter("show_support"))
async def support(_, callback_query: CallbackQuery) -> None:
    localization = await locale_load(callback_query.from_user)
    admins = await db_interface.support_get()
    await callback_query.edit_message_text(
        localization["support-message"].format(
            support=normalize_admins(admins)
        ),
        reply_markup=support_kb(localization)
    )


# To start callback

@bot.on_callback_query(filters=callback_data_filter("to_start"))
async def to_start(client: Client, callback_query: CallbackQuery) -> None:
    localization = await locale_load(callback_query.from_user)
    await callback_query.edit_message_text(
        localization["start-message"],
        reply_markup=start_kb(localization)
    )
    logger.info(f"User @{callback_query.from_user.username} returned to start")


# Start command

@bot.on_message(filters=filters.command(["start", "help"]))
async def start(client: Client, message: Message) -> None:
    localization = await locale_load(message.from_user)
    
    await client.send_sticker(message.chat.id, "Static/sticker.webp")
    await client.send_message(
        message.chat.id,
        localization["start-message"],
        reply_markup=start_kb(localization)
    )
    
    is_exist = await db_interface.check_user(message.from_user.id)
    if not is_exist:
        lang = lang_detection.detect(message.from_user.phone_number)
        await db_interface.new_user(message.from_user.id, lang)

    logger.info(f"Greeting message was sent to @{message.from_user.username}")


# Run application

if __name__ == "__main__":
    try:
        logger.debug("Starting bot...")
        bot.run()
        
    except:
        logger.exception("Unexpected error")
        raise
