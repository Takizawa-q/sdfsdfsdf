from aiogram.types.message import Message
from loader import bot, dp
import re
from aiogram import types
from MySQL import SQL
from reply_texts import WBCON_LINK
import json
from Handlers.catch_services import services_cb
from aiogram.utils.callback_data import CallbackData


parsing_cb_ali = CallbackData('parsing_tnved', 'action')

@dp.callback_query_handler(services_cb.filter(action="tnved"))
async def send_message(query: types.CallbackQuery, callback_data: dict):
    user_id = query.from_user.id
    SQL().set_sm_tnved_1(user_id)
    await bot.edit_message_text("Отправь текст с наименованием нужного товара(например \"Майка\")", user_id, query.message.message_id)


async def tnved_send_message(message: types.Message, message_text):
    user_id = message.from_user.id
    parsing_left_count = SQL().get_parsing_left_count(user_id)
    if parsing_left_count > 0:
        await message.answer(f"Ждите результат, скоро он придёт в чат сообщением(ТНВЭД в порядке очереди)\nОсталось попыток: {parsing_left_count - 1} из 200 на сегодняшний день")
        try:
            text_to_send = f"Результат по запросу: <b>{message_text}</b>"

            SQL().update_parsing_left_count(user_id, parsing_left_count, amount=1)
            data = SQL().POST_TNVED_REQUEST(message_text, user_id)
            for dat in data:
                prob = int(dat["probability"])
                if prob > 2:
                    text_to_send += f"""
Вероятность в %: <b>{int(prob)}</b>

Код ТНВЭД: <b>{dat["code"]}</b>

Описание: <b>{dat["description"]}</b>

НДС: <b>{dat["nds"]}</b>

<i>Попыток осталось: <b>{parsing_left_count - 1}</b></i>
        """
                    await message.answer(str(text_to_send), parse_mode="HTML")
                    text_to_send = ""
            if text_to_send != "":
                await message.answer("По вашему запросу не найден подходящий ТН ВЭД")
                parsing_left_count = SQL().get_parsing_left_count(user_id)
                SQL().update_parsing_left_count(user_id, parsing_left_count, -1)
        except Exception as e:
            print(e)
            await message.answer(f"Просим прощения, но по твоему запросу не удалось ничего найти😔 Но мы вернули тебе попытку!", parse_mode="HTML")
            parsing_left_count = SQL().get_parsing_left_count(user_id)
            SQL().update_parsing_left_count(user_id, parsing_left_count, -1)
    else:
        await message.answer(f"Извини, но у тебя закончились попытки😔 Советуем посетить наш сайт <b>{WBCON_LINK}</b>, где вы сможете купить безлимитную версию парсера, которая может парсить не только артикулы, но и категории, поисковые запросы, бренды и поставщиков!\nhttps://wbcon.ru/parser-ozon/",
                                    parse_mode="HTML")