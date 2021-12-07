from os import name
from aiogram.types.message import Message
from aiogram.utils.markdown import text
from loader import bot, dp
import re
from aiogram import types
from MySQL import SQL
from reply_texts import WBCON_LINK
import json
from Handlers.catch_services import services_cb
from aiogram.utils.callback_data import CallbackData


@dp.callback_query_handler(services_cb.filter(action="inn"))
async def send_message(query: types.CallbackQuery, callback_data: dict):
    user_id = query.from_user.id
    SQL().set_sm_inn_1(user_id)
    await bot.edit_message_text("Отправь ИНН или ОГРН:", user_id, query.message.message_id)

async def inn_send_message(message: types.Message, message_text):
    user_id = message.from_user.id
    parsing_left_count = SQL().get_parsing_left_count(user_id)
    SQL().update_parsing_left_count(user_id, parsing_left_count, 1)
    if parsing_left_count > 0:
        try:
            await message.answer(f"Ждите результат, скоро он придёт в чат сообщением(ИНН в порядке очереди)\nОсталось попыток: {parsing_left_count - 1} из 200 на сегодняшний день")
            data = SQL().POST_INN_REQUEST(message_text, user_id)
            text_to_send = f"<i>Результат по запросу: {message_text}</i>\n"
            for i in data:
                dat = data[i]
                if i == "name" and dat != '':
                    text_to_send += f"Название компании: <b>{dat}</b>" + "\n"
                elif i == "reg_date" and dat != '':
                    text_to_send += f"Дата регистрации: <b>{dat}</b>" + "\n"
                elif i == "full_name" and dat != '':
                    text_to_send += f"Полное название: <b>{dat}</b>" + "\n"
                elif i == "inn" and dat != '':
                    text_to_send += f"ИНН: <b>{dat}</b>" + "\n"
                elif i == "kpp" and dat != '':
                    text_to_send += f"КПП: <b>{dat}</b>" + "\n"
                elif i == "ogrn" and dat != '':
                    text_to_send += f"ОГРН: <b>{dat}</b>" + "\n"
                elif i == "ogrn_date" and dat != '':
                    text_to_send += f"Дата ОГРН: <b>{dat}</b>" + "\n"
                elif i == "dolgnost" and dat != '':
                    text_to_send += f"Должность: <b>{dat}</b>" + "\n"
                elif i == "director_name" and dat != '':
                    text_to_send += f"ФИО руководителя: <b>{dat}</b>" + "\n"
                elif i == "director_time" and dat != '':
                    text_to_send += f"Руководитель с даты: <b>{dat}</b>" + "\n"
                elif i == "main_work" and dat != '':
                    text_to_send += f"Сфера занятости: <b>{dat}</b>" + "\n"
                elif i == "main_okved" and dat != '':
                    text_to_send += f"Основной ОКВЭД: <b>{dat}</b>" + "\n"
                elif i == "average_number" and dat != '':
                    text_to_send += f"Средняя численность сотрудников: <b>{dat}</b>" + "\n"
                elif i == "revenue" and dat != '':
                    text_to_send += f"Доход: <b>{dat}</b>" + "\n"
                elif i == "profit" and dat != '':
                    text_to_send += f"Прибыль: <b>{dat}</b>" + "\n"
                elif i == "reliability" and dat != '':
                    text_to_send += f"Надёжность: <b>{dat}</b>" + "\n"
                elif i == "authorized_capital" and dat != '':
                    text_to_send += f"Уставной капитал: <b>{dat}</b>" + "\n"
                elif i == "legal_adress" and dat != '':
                    text_to_send += f"Юридический адрес: <b>{dat}</b>" + "\n"
                elif i == "usn" and dat != '':
                    text_to_send += f"Упрощенная система налогообложения: <b>{dat}</b>" + "\n"
                elif i == "msp" and dat != '':
                    text_to_send += f"Входит ли в реестр субъектов малого и среднего: <b>{dat}</b>" + "\n"
                elif i == "taxes" and dat != '':
                    text_to_send += f"Налоги: <b>{dat}</b>" + "\n"
                elif i == "contributions" and dat != '':
                    text_to_send += f"Взносы: <b>{dat}</b>" + "\n"
                elif i == "founders_" and dat != '':
                    text_to_send += f"Учредители: <b>{dat}</b>" + "\n"
                elif i == "email" and dat != '':
                    text_to_send += f"EMAIL: <b>{dat}</b>" + "\n"
                elif i == "phones" and dat != '':
                    text_to_send += f"Телефон: <b>{dat}</b>" + "\n"
            await message.answer(text_to_send, parse_mode="HTML")
        except Exception as e:
            print(e)
            await message.answer(f"Просим прощения, но по твоему запросу не удалось ничего найти😔 Но мы вернули тебе попытку!", parse_mode="HTML")
            parsing_left_count = SQL().get_parsing_left_count(user_id)
            SQL().update_parsing_left_count(user_id, parsing_left_count, -1)
    else:
        await message.answer(f"Извини, но у тебя закончились попытки😔 Советуем посетить наш сайт <b>{WBCON_LINK}</b>, где вы сможете купить безлимитную версию парсера, которая может парсить не только артикулы, но и категории, поисковые запросы, бренды и поставщиков!\nhttps://wbcon.ru/parser-ozon/",
                                    parse_mode="HTML")