from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


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
                  localization["inline-to-settings"],
                  callback_data="to_settings"
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