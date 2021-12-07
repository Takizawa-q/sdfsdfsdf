from loader import bot, dp
import re
from aiogram import types
from reply_texts import help_text
from MySQL import SQL


@dp.message_handler(lambda message: message.text == "Помощь 🕵️" or message.text == "/help")
async def send_message(message: types.Message):
    # SQL().update_sm_ozon(message.from_user.id, 0)
    # SQL().update_sm_wildberries(message.from_user.id, 0)
    await message.answer(help_text, parse_mode="HTML", disable_web_page_preview=True)