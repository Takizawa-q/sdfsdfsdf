from ast import parse
from aiogram.dispatcher import storage
from aiogram.types.message import Message
from aiogram.utils.markdown import text
from loader import bot, dp
import re
from aiogram import types
from MySQL import SQL
from reply_texts import WBCON_LINK
import json
from aiogram.utils.callback_data import CallbackData

async def lamoda_send_message(message: types.Message):
    message_text = message.text
    if not message_text.startswith("https://"):
        message_text = f"https://www.lamoda.ru/p/{message.text}"
    user_id = message.from_user.id
    parsing_left_count = SQL().get_parsing_left_count(user_id)
    
    if parsing_left_count > 0:
        SQL().update_parsing_left_count(user_id, parsing_left_count, 1)
        await message.answer(f"Ждите результат, скоро он придёт в чат сообщением(Lamoda в порядке очереди)\nОсталось попыток: {parsing_left_count - 1} из 200 на сегодняшний день")
        try:
            ud = json.loads(SQL().POST_LAMODA_REQUEST(message_text, user_id))
            item_name = ud["item"]
            item_url = ud["item_url"]
            description = ud["description"]
            complectation = ud["complectation"]
            gender = ud["gender"]
            brand = ud["brand"]
            rating = ud["rating"]
            reviews_count = ud["reviews_count"]
            price_with_discount = ud["price"]
            price_withoud_discount = ud["old_price"]
            discount_percent = ud["discount"]
            discount_amount = ud["discount_lamoda"]
            color = ud["colors"]
            images = ud["images"]
            sizes = ud["sizes"].replace(",", " ед.,")
            if sizes:
                sizes += "ед."
            
            quantity = ud["all_quantities"]
            
            text_to_send = f"""Результат по запросу: <i>{message_text}</i>
            Название: <b>{item_name}</b>
            Бренд: <b>{brand}</b>
            Рейтинг: <b>{rating}</b>
            Кол-во отзывов: <b>{reviews_count}</b>
            Цена со скидкой: <b>{price_with_discount}</b>
            Цена без скидки: <b>{price_withoud_discount}</b>
            Скидка в %: <b>{discount_percent}</b>
            Размер скидки: <b>{discount_amount}</b>
            Цвет: <b>{color}</b>
            Пол: <b>{gender}</b>
            Описание: <b>{description}</b>
            Комплектация: <b>{complectation}</b>
            
            Ссылка на изображения: <b>{images}</b>
            Ссылка на товар: <b>{item_url}</b>
            """
            storages_text_to_send = f"""
            <i>Кол-во по размерам: <b>{sizes}</b></i>
<i>Общее кол-во: <b>{quantity}</b></i>
            """
            await message.answer(str(text_to_send), parse_mode="HTML")
            await message.answer(str(storages_text_to_send), parse_mode="HTML")
        except Exception:
            await message.answer(f"Просим прощения, но по твоему запросу не удалось ничего найти😔 Но мы вернули тебе попытку!", parse_mode="HTML")
            parsing_left_count = SQL().get_parsing_left_count(user_id)
            SQL().update_parsing_left_count(user_id, parsing_left_count, -1)
    else:
        await message.answer(f"Извини, но у тебя закончились попытки😔 Советуем посетить наш сайт <b>{WBCON_LINK}</b>, где вы сможете купить безлимитную версию парсера, которая может парсить не только артикулы, но и категории, поисковые запросы, бренды и поставщиков!\nhttps://wbcon.ru/parser-ozon/",
                                    parse_mode="HTML")
    

    
    
    