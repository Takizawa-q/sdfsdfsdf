from aiogram.types.message import Message
from loader import bot, dp
import re
import json
from aiogram import types
from MySQL import SQL
from reply_texts import WBCON_LINK
from aiogram.utils.callback_data import CallbackData

parsing_cb_ali = CallbackData('parsing_ali', 'action')

async def ali_send_message(message: types.Message, message_text):
    user_id = message.from_user.id
    parsing_left_count = SQL().get_parsing_left_count(user_id)
    if parsing_left_count > 0:
        try:
            print(message_text)
            data = json.loads(SQL().POST_ALI_REQUEST(user_id, message_text))[1]
            await message.answer(f"Ждите результат, скоро он придёт в чат сообщением(Aliexpress в порядке очереди)\nОсталось попыток: {parsing_left_count - 1} из 200 на сегодняшний день")
            price_w_d = data["minActivityAmount"]
            bought_count = data["tradeCount"]
            
            text_to_send = f"""Результат по запросу: <b>{message_text}</b>
Название: <b>{data["title"]}</b>
Дерево Категорий: <b>{data["category_tree"]}</b>
Артикул: <b>{data["productId"]}</b>
Имя проадавца: <b>{data["storeName"]}</b>
Ссылка на продавца: <b>{data["storeUrl"]}</b>
Рейтинг: <b>{data["rating"]}</b>
Цена со скидкой: <b>{price_w_d}</b>
Цена без скидки: <b>{data["originalPrice"]}</b>
Скидка в %: <b>{data["discount"]}</b>
Кол-во товара: <i><b>{data["totalAvailQuantity"]}</b></i>
Кол-во заказов: <i><b>{bought_count}</b></i>
Выкупили на общую сумму: <i><b>{int(int(price_w_d) * int(bought_count))}</b></i>
Ссылка на изображение: <b>{data["imagePathList"].split(", ")[0]}</b>
Ссылка на товар: <b>{data["productDetailUrl"]}</b>
"""
            await message.answer(str(text_to_send), parse_mode="HTML")
            SQL().update_parsing_left_count(user_id, parsing_left_count, amount=1)
            SQL().create_user_request(user_id, message_text)
        except Exception as e:
            print(e)
            await message.answer(f"Просим прощения, но по твоему запросу не удалось ничего найти😔 Но мы вернули тебе попытку!", parse_mode="HTML")
            parsing_left_count = SQL().get_parsing_left_count(user_id)
            SQL().update_parsing_left_count(user_id, parsing_left_count, -1)
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