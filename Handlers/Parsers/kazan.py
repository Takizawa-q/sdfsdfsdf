from aiogram.types.message import Message
from loader import bot, dp
import re
from aiogram import types
from MySQL import SQL
from reply_texts import WBCON_LINK
import json
from aiogram.utils.callback_data import CallbackData


parsing_cb_ali = CallbackData('parsing_ali', 'action')

async def kazan_send_message(message: types.Message, message_text):
    user_id = message.from_user.id
    parsing_left_count = SQL().get_parsing_left_count(user_id)
    if parsing_left_count > 0:
        await message.answer(f"Ждите результат, скоро он придёт в чат сообщением(Kazan в порядке очереди)\nОсталось попыток: {parsing_left_count - 1} из 200 на сегодняшний день")
        try:
            print(message_text)
            SQL().update_parsing_left_count(user_id, parsing_left_count, amount=1)
            data = json.loads(SQL().POST_KAZAN_REQUEST(message_text, user_id))[1]
            print(data)
            if message_text.startswith("https://kazanexpress.ru/product"):
                product_link = message_text
            else:
                product_link = "https://kazanexpress.ru/product/" + str(message_text)
            photo_urls = data["photo_high_urls"]
            if "," in photo_urls:
                photo_url = photo_urls.split(",")[0]
            else:
                photo_url = photo_urls
            price_w_d = data["fullprice"]
            orders_count = data["ordersquantity"]
            text_to_send = f"""Результат по запросу: <b><i>{message_text}</i></b>
    Название: <b>{data["item_name"]}</b>
    Артикул: <b>{data["item_id"]}</b>
    Продавец: <b>{data["seller"]}</b>
    Цена без скидки: <b>{price_w_d}</b>
    Цена со скидкой: <b>{data["purchaseprice"]}</b>
    Рейтинг: <b>{data["item_rating"]}</b>
    Описание: <b>{data["description"]}</b>
    Характеристика: <b>{data["attributes"]}</b>
    Кол-во остатков: <i><b>{data["available_amount"]}</b></i>
    Кол-во заказов: <i><b>{orders_count}</b></i>
    Выкупили на сумму: <i><b>{int(int(price_w_d) * int(orders_count))}</b></i>
    Ссылка на товар: <b>{product_link}</b>
    Ссылка на изображение: <b>{photo_url}</b>
    """

            await message.answer(str(text_to_send), parse_mode="HTML")
        except:
            await message.answer(f"Просим прощения, но по твоему запросу не удалось ничего найти😔 Но мы вернули тебе попытку!", parse_mode="HTML")
            parsing_left_count = SQL().get_parsing_left_count(user_id)
            SQL().update_parsing_left_count(user_id, parsing_left_count, -1)
    else:
        await message.answer(f"Извини, но у тебя закончились попытки😔 Советуем посетить наш сайт <b>{WBCON_LINK}</b>, где вы сможете купить безлимитную версию парсера, которая может парсить не только артикулы, но и категории, поисковые запросы, бренды и поставщиков!\nhttps://wbcon.ru/parser-ozon/",
                                    parse_mode="HTML")