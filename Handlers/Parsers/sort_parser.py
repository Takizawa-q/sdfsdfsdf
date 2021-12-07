from ast import parse
from aiogram.dispatcher import storage
from aiogram.types.message import Message
from aiogram.utils.markdown import text
from Handlers.Services.inn import inn_send_message
from loader import bot, dp
import re
from aiogram import types
from MySQL import SQL
from Handlers.Parsers.lamoda import lamoda_send_message
from Handlers.Parsers.wb import wb_send_message
from Handlers.Parsers.ozon import ozon_send_message
from Handlers.Parsers.sber import sber_send_message
from Handlers.Parsers.kazan import kazan_send_message
from Handlers.Parsers.ali import ali_send_message
from Handlers.Services.tnved import tnved_send_message
from Handlers.Services.inn import inn_send_message
from reply_texts import WBCON_LINK
import json
from aiogram.utils.callback_data import CallbackData


@dp.message_handler(lambda message: message.text.isdigit() or message.text.startswith("https://www.ozon.ru/product/") or message.text.startswith("https://www.ozon.ru/products/") or message.text.startswith("https://www.wildberries.ru/catalog") or message.text.startswith("https://wildberries.ru/catalog") or message.text.isalnum() or message.text.startswith("https://www.lamoda.ru/p") or message.text.startswith("https://sbermegamarket.ru/catalog") or message.text.startswith("https://kazanexpress.ru/product/") or message.text.startswith("https://aliexpress.ru/item/"))
async def send_message(message: types.Message):
    user_id = message.from_user.id
    message_text = message.text
    if SQL().get_sm_wildberries(user_id) == 1:
        if message_text.startswith("https://www.wildberries.ru/catalog") or message_text.startswith('https://wildberries.ru/catalog') or message_text.isdigit():
            await wb_send_message(message)
    
    elif SQL().get_sm_ozon(user_id) == 1:
        if message_text.startswith("https://www.ozon.ru/product/") or message_text.startswith("https://www.ozon.ru/products/")or message_text.isdigit():
            if message_text.startswith("https://www.ozon.ru/products/"):
                message_text = re.search("https://www\.ozon\.ru/products/(\d*)",  str(message_text)).group(1)
            await ozon_send_message(message, message_text)
    
    elif SQL().get_sm_lamoda(user_id) == 1 and not message_text.isdigit():
        await lamoda_send_message(message)
    
    elif SQL().get_sm_sber(user_id) == 1:
        await sber_send_message(message)
    
    elif SQL().get_sm_ali(user_id) == 1:
        if message_text.isdigit():
            message_text = "https://aliexpress.ru/item/" + message_text
        else:
            pass
        await ali_send_message(message, message_text)
    
    elif SQL().get_sm_kazan(user_id) == 1:
        if message_text.startswith("https://kazanexpress.ru/product/"):
            pass
        else:
            message_text = re.search("(\d*)", message_text).group(1)
        await kazan_send_message(message, message_text)

    elif SQL().get_sm_inn(user_id) == 1:
        await inn_send_message(message, message_text)
    else:
        await tnved_send_message(message, message_text)