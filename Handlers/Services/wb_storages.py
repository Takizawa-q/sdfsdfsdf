from time import sleep
from operator import itemgetter
from ast import literal_eval
from datetime import date
from MySQL import SQL
import requests
from datetime import datetime
from loader import bot, dp
from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from reply_texts import WBCON_LINK, WBCON_STORAGES_LINK
from Handlers.catch_services import services_cb

wb_storage = CallbackData('storages', 'action')


@dp.callback_query_handler(services_cb.filter(action="wb_storages"))
async def send_message(query: types.CallbackQuery, callback_data: dict):
    user_id = query.from_user.id
    kb = InlineKeyboardMarkup().row(
        InlineKeyboardButton(
            "Подольск", callback_data=wb_storage.new(action="Podolsk"))
    ).row(InlineKeyboardButton("Коледино", callback_data=wb_storage.new(action="Koledino"))).row(
        InlineKeyboardButton(
            "Электросталь", callback_data=wb_storage.new(action="Elektro"))
    ).row(InlineKeyboardButton("Электросталь КБТ", callback_data=wb_storage.new(action="ElektroKBT"))).row(
        InlineKeyboardButton(
            "Санкт-Петербург", callback_data=wb_storage.new(action="Piter"))
    ).row(InlineKeyboardButton("Екатеринбург", callback_data=wb_storage.new(action="Ekat"))).row(
        InlineKeyboardButton(
            "Новосибирск", callback_data=wb_storage.new(action="Novosib"))
    ).row(InlineKeyboardButton("Краснодар", callback_data=wb_storage.new(action="Krasnodar"))).row(
        InlineKeyboardButton(
            "Хабаровск", callback_data=wb_storage.new(action="Habarovsk"))
    ).row(InlineKeyboardButton("Казань", callback_data=wb_storage.new(action="Kazan")))
    await bot.edit_message_text("Выбери нужный тебе склад:", user_id, query.message.message_id, reply_markup=kb)

def return_text_to_send(data):
    time_lst = []
    send_text = ""
    for dat in data[1:]:
        time_lst.append([datetime.strptime(dat["date"].split('T')[0], "%Y-%m-%d"), dat["all"], dat["mix"], dat["mono"], dat["monoPallet"], dat["superSafe"]])
    time_lst = sorted(time_lst, key=lambda x: x[0])
    for time, all, mix, mono, monop, supersafe in time_lst:
        send_text += f"Дата: <b>{str(time).split(' ')[0]}</b> | Всего: <b>{all}</b> | Микс: <b>{mix}</b> | Моно: <b>{mono}</b> | Монопаллет: <b>{monop}</b> | Суперсейф: <b>{supersafe}</b>\n"
    return send_text
        
    
    
@dp.callback_query_handler(wb_storage.filter(action="Podolsk"))
async def send_message(query: types.CallbackQuery, callback_data: dict):
    user_id = query.from_user.id
    data = literal_eval(requests.get(
        "http://188.120.255.121:5555/put/507").text)
    text_to_send = "Результат по Подольску:\n"
    send_text = return_text_to_send(data)
    text_to_send += send_text
    text_to_send += f"Сервис также доступен на сайте {WBCON_STORAGES_LINK}"
    parsing_left_count = SQL().get_parsing_left_count(user_id)
    SQL().update_parsing_left_count(user_id, parsing_left_count, 1)
    text_to_send += f"\n<i>Попыток осталось</i>: {parsing_left_count - 1}"
    await bot.edit_message_text(text_to_send, user_id, query.message.message_id, parse_mode="HTML", disable_web_page_preview=True)


@dp.callback_query_handler(wb_storage.filter(action="Koledino"))
async def send_message(query: types.CallbackQuery, callback_data: dict):
    user_id = query.from_user.id
    data = literal_eval(requests.get(
        "http://188.120.255.121:5555/put/3158").text)
    text_to_send = "Результат по Коледино:\n"
    send_text = return_text_to_send(data)
    text_to_send += send_text
    text_to_send += f"Сервис также доступен на сайте {WBCON_STORAGES_LINK}"
    parsing_left_count = SQL().get_parsing_left_count(user_id)
    SQL().update_parsing_left_count(user_id, parsing_left_count, 1)
    text_to_send += f"\n<i>Попыток осталось</i>: {parsing_left_count - 1}"
    await bot.edit_message_text(text_to_send, user_id, query.message.message_id, parse_mode="HTML", disable_web_page_preview=True)


@dp.callback_query_handler(wb_storage.filter(action="Novosib"))
async def send_message(query: types.CallbackQuery, callback_data: dict):
    user_id = query.from_user.id
    data = literal_eval(requests.get(
        "http://188.120.255.121:5555/put/686").text)
    text_to_send = "Результат по Новосибирску:\n"
    send_text = return_text_to_send(data)
    text_to_send += send_text
    text_to_send += f"Сервис также доступен на сайте {WBCON_STORAGES_LINK}"
    parsing_left_count = SQL().get_parsing_left_count(user_id)
    SQL().update_parsing_left_count(user_id, parsing_left_count, 1)
    text_to_send += f"\n<i>Попыток осталось</i>: {parsing_left_count - 1}"
    await bot.edit_message_text(text_to_send, user_id, query.message.message_id, parse_mode="HTML", disable_web_page_preview=True)


@dp.callback_query_handler(wb_storage.filter(action="Krasnodar"))
async def send_message(query: types.CallbackQuery, callback_data: dict):
    user_id = query.from_user.id
    data = literal_eval(requests.get(
        "http://188.120.255.121:5555/put/130744").text)
    text_to_send = "Результат по Краснодару:\n"
    send_text = return_text_to_send(data)
    text_to_send += send_text
    text_to_send += f"Сервис также доступен на сайте {WBCON_STORAGES_LINK}"
    parsing_left_count = SQL().get_parsing_left_count(user_id)
    SQL().update_parsing_left_count(user_id, parsing_left_count, 1)
    text_to_send += f"\n<i>Попыток осталось</i>: {parsing_left_count - 1}"
    await bot.edit_message_text(text_to_send, user_id, query.message.message_id, parse_mode="HTML", disable_web_page_preview=True)


@dp.callback_query_handler(wb_storage.filter(action="Elektro"))
async def send_message(query: types.CallbackQuery, callback_data: dict):
    user_id = query.from_user.id
    data = literal_eval(requests.get(
        "http://188.120.255.121:5555/put/120762").text)
    text_to_send = "Результат по Электростали\n"
    send_text = return_text_to_send(data)
    text_to_send += send_text
    text_to_send += f"Сервис также доступен на сайте {WBCON_STORAGES_LINK}"
    parsing_left_count = SQL().get_parsing_left_count(user_id)
    SQL().update_parsing_left_count(user_id, parsing_left_count, 1)
    text_to_send += f"\n<i>Попыток осталось</i>: {parsing_left_count - 1}"
    await bot.edit_message_text(text_to_send, user_id, query.message.message_id, parse_mode="HTML", disable_web_page_preview=True)


@dp.callback_query_handler(wb_storage.filter(action="Habarovsk"))
async def send_message(query: types.CallbackQuery, callback_data: dict):
    user_id = query.from_user.id
    data = literal_eval(requests.get(
        "http://188.120.255.121:5555/put/1193").text)
    text_to_send = "Результат по Хабаровску:\n"
    send_text = return_text_to_send(data)
    text_to_send += send_text
    text_to_send += f"Сервис также доступен на сайте {WBCON_STORAGES_LINK}"
    parsing_left_count = SQL().get_parsing_left_count(user_id)
    SQL().update_parsing_left_count(user_id, parsing_left_count, 1)
    text_to_send += f"\n<i>Попыток осталось</i>: {parsing_left_count - 1}"
    await bot.edit_message_text(text_to_send, user_id, query.message.message_id, parse_mode="HTML", disable_web_page_preview=True)


@dp.callback_query_handler(wb_storage.filter(action="ElektroKBT"))
async def send_message(query: types.CallbackQuery, callback_data: dict):
    user_id = query.from_user.id
    data = literal_eval(requests.get(
        "http://188.120.255.121:5555/put/121709").text)
    text_to_send = "Результат по Электростали-КБТ:\n"
    send_text = return_text_to_send(data)
    text_to_send += send_text
    text_to_send += f"Сервис также доступен на сайте {WBCON_STORAGES_LINK}"
    parsing_left_count = SQL().get_parsing_left_count(user_id)
    SQL().update_parsing_left_count(user_id, parsing_left_count, 1)
    text_to_send += f"\n<i>Попыток осталось</i>: {parsing_left_count - 1}"
    await bot.edit_message_text(text_to_send, user_id, query.message.message_id, parse_mode="HTML", disable_web_page_preview=True)


@dp.callback_query_handler(wb_storage.filter(action="Kazan"))
async def send_message(query: types.CallbackQuery, callback_data: dict):
    user_id = query.from_user.id
    data = literal_eval(requests.get(
        "http://188.120.255.121:5555/put/117986").text)
    text_to_send = "Результат по Казани:\n"
    send_text = return_text_to_send(data)
    text_to_send += send_text
    text_to_send += f"Сервис также доступен на сайте {WBCON_STORAGES_LINK}"
    parsing_left_count = SQL().get_parsing_left_count(user_id)
    SQL().update_parsing_left_count(user_id, parsing_left_count, 1)
    text_to_send += f"\n<i>Попыток осталось</i>: {parsing_left_count - 1}"
    await bot.edit_message_text(text_to_send, user_id, query.message.message_id, parse_mode="HTML", disable_web_page_preview=True)


@dp.callback_query_handler(wb_storage.filter(action="ElektroKBT"))
async def send_message(query: types.CallbackQuery, callback_data: dict):
    user_id = query.from_user.id
    data = literal_eval(requests.get(
        "http://188.120.255.121:5555/put/121709").text)
    text_to_send = "Результат по Электростали-КБТ:\n"
    send_text = return_text_to_send(data)
    text_to_send += send_text
    text_to_send += f"Сервис также доступен на сайте {WBCON_STORAGES_LINK}"
    parsing_left_count = SQL().get_parsing_left_count(user_id)
    SQL().update_parsing_left_count(user_id, parsing_left_count, 1)
    text_to_send += f"\n<i>Попыток осталось</i>: {parsing_left_count - 1}"
    await bot.edit_message_text(text_to_send, user_id, query.message.message_id, parse_mode="HTML", disable_web_page_preview=True)


@dp.callback_query_handler(wb_storage.filter(action="Piter"))
async def send_message(query: types.CallbackQuery, callback_data: dict):
    user_id = query.from_user.id
    data = literal_eval(requests.get(
        "http://188.120.255.121:5555/put/2737").text)
    text_to_send = "Результат по Санкт-Петербургу:\n"
    send_text = return_text_to_send(data)
    text_to_send += send_text
    text_to_send += f"Сервис также доступен на сайте {WBCON_STORAGES_LINK}"
    parsing_left_count = SQL().get_parsing_left_count(user_id)
    SQL().update_parsing_left_count(user_id, parsing_left_count, 1)
    text_to_send += f"\n<i>Попыток осталось</i>: {parsing_left_count - 1}"
    await bot.edit_message_text(text_to_send, user_id, query.message.message_id, parse_mode="HTML", disable_web_page_preview=True)


@dp.callback_query_handler(wb_storage.filter(action="Ekat"))
async def send_message(query: types.CallbackQuery, callback_data: dict):
    user_id = query.from_user.id
    data = literal_eval(requests.get(
        "http://188.120.255.121:5555/put/1733").text)
    text_to_send = "Результат по Екатеринбургу:\n"
    send_text = return_text_to_send(data)
    text_to_send += send_text
    text_to_send += f"Сервис также доступен на сайте {WBCON_STORAGES_LINK}"
    parsing_left_count = SQL().get_parsing_left_count(user_id)
    SQL().update_parsing_left_count(user_id, parsing_left_count, 1)
    text_to_send += f"\n<i>Попыток осталось</i>: {parsing_left_count - 1}"
    await bot.edit_message_text(text_to_send, user_id, query.message.message_id, parse_mode="HTML", disable_web_page_preview=True)
