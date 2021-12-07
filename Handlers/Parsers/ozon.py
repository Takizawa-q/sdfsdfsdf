from aiogram.types.message import Message
from loader import bot, dp
import re
from aiogram import types
from MySQL import SQL
from reply_texts import WBCON_LINK
from aiogram.utils.callback_data import CallbackData

parsing_cb_ozon = CallbackData('parsing_ozon', 'action')

async def ozon_send_message(message: types.Message, message_text):
    user_id = message.from_user.id
    parsing_left_count = SQL().get_parsing_left_count(user_id)
    if parsing_left_count > 0:
        await message.answer(f"Ждите результат, скоро он придёт в чат сообщением(Ozon в порядке очереди)\nОсталось попыток: {parsing_left_count - 1} из 200 на сегодняшний день")

        SQL().update_parsing_left_count(user_id, parsing_left_count, amount=1)
        SQL().create_user_request(user_id, message_text)
    else:
        await message.answer(f"Извини, но у тебя закончились попытки😔 Советуем посетить наш сайт <b>{WBCON_LINK}</b>, где вы сможете купить безлимитную версию парсера, которая может парсить не только артикулы, но и категории, поисковые запросы, бренды и поставщиков!\nhttps://wbcon.ru/parser-ozon/",
                                    parse_mode="HTML")

# @dp.callback_query_handler(parsing_cb_ozon.filter(action='NoOzon'))
# async def send_message(query: types.CallbackQuery, callback_data: dict):
#     await bot.edit_message_text("Отправь сюда Артикул или ссылку на товар с Ozon:",
#                                 query.from_user.id,
#                                 query.message.message_id,
#                                 parse_mode="HTML"
#                                 )