from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.types.bots_and_keyboards import keyboard_button


def start_kb(localization: dict[str, str]) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    localization["inline-account"],
                    callback_data="show_account"
                ),
                InlineKeyboardButton(
                    localization["inline-support"],
                    callback_data="show_support"
                )
            ],
            [
                InlineKeyboardButton(
                    localization["inline-price"],
                    callback_data="show_price"
                )
            ]
        ]
    )
    return keyboard


def account_kb(localization: dict[str, str]) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        [
            [
              InlineKeyboardButton(
                  localization["inline-settings"],
                  callback_data="show_settings"
              )  
            ],
            [
                InlineKeyboardButton(
                    localization["inline-to-start"],
                    callback_data="to_start"
                )
            ]
        ]
    )
    return keyboard


def settings_kb(localization: dict[str, str]) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    localization["inline-language-settings"],
                    callback_data="settings_lang"
                )
            ],
            [
                InlineKeyboardButton(
                    localization["inline-account"],
                    callback_data="show_account"
                )
            ]
        ]
    )
    return keyboard


def lang_kb(localization: dict[str, str]) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    localization["inline-set-lang-ru"],
                    callback_data="set_lang_ru"
                ),
                InlineKeyboardButton(
                    localization["inline-set-lang-en"],
                    callback_data="set_lang_en"
                )
            ]
        ]
    )
    return keyboard


def support_kb(localization: dict[str, str]) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    localization["inline-to-start"],
                    callback_data="to_start"
                )
            ]
        ]
    )
    return keyboard