from .buttons import *
from aiogram.types import ReplyKeyboardMarkup

# EXCEL_TXT_CHAT = ReplyKeyboardMarkup(resize_keyboard=True).insert(
#     excel_button).insert(txt_button).row(chat_button).row(back_button)

MAIN_MENU_BUTTON = ReplyKeyboardMarkup(resize_keyboard=True).insert(
    parsers_button).insert(services_button).row(help_button)

BACK_BUTTON = ReplyKeyboardMarkup(resize_keyboard=True).insert(back_button)

HELP_BUTTON = ReplyKeyboardMarkup(resize_keyboard=True).insert(help_button)


