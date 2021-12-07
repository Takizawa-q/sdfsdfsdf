from time import sleep
from operator import itemgetter
from ast import literal_eval
from datetime import date

from aiogram.utils.markdown import text
from MySQL import SQL

import requests
import json
from datetime import datetime
from loader import bot, dp
from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from reply_texts import WBCON_GEO_LINK
from Handlers.catch_services import services_cb

STORAGES = {"117501": "Подольск", "507": "Коледино", "686": "Новосибирск", "1193": "Хабаровск", "1699": "Краснодар старый", "130744": "Краснодар новый", "1733": "Екатеринбург", "2737": "Санкт-Петербург", "117986": "Казань", "115577": "Крекшино", "116433": "Домодедово", "120602": "Электросталь КБТ", "120762": "Электросталь"}

wb_geo = CallbackData('location', 'action')

@dp.callback_query_handler(services_cb.filter(action="wb_geo"))
async def send_message(query: types.CallbackQuery, callback_data: dict):
    user_id = query.from_user.id
    kb = InlineKeyboardMarkup().row(
        InlineKeyboardButton(
            "Москва", callback_data=wb_geo.new(action="msk"))
    ).row(InlineKeyboardButton("Санкт-Петербург", callback_data=wb_geo.new(action="spb"))).row(
        InlineKeyboardButton(
            "Екатеринбург", callback_data=wb_geo.new(action="ekat"))
    ).row(InlineKeyboardButton("Новосибирск", callback_data=wb_geo.new(action="novosib"))).row(
        InlineKeyboardButton(
            "Краснодар", callback_data=wb_geo.new(action="krasnodar"))
    ).row(InlineKeyboardButton("Хабаровск", callback_data=wb_geo.new(action="habar"))).row(
        InlineKeyboardButton(
            "Казань", callback_data=wb_geo.new(action="kazan"))
    ).row(InlineKeyboardButton("Беларусь", callback_data=wb_geo.new(action="belarus"))).row(
        InlineKeyboardButton(
            "Казахстан", callback_data=wb_geo.new(action="kazah"))
    ).row(InlineKeyboardButton("Армения", callback_data=wb_geo.new(action="armenia"))).row(
        InlineKeyboardButton("Киргизия", callback_data=wb_geo.new(action="kirgiz"))
    )
    await bot.edit_message_text("Выберите ГЕО вашего покупателя и узнайте склады по приоритетности:", user_id, query.message.message_id, reply_markup=kb)

def create_user_text(data, user_id, txt):
    text_to_send = f"Приоритетность складов для ГЕО {txt}:\n"
    for dat in json.loads(data):
        store = STORAGES[str(dat["storeId"])]
        deliv = dat["deliveryOption"]
        prior = dat["priority"]
        in_days = dat["inDays"]
        text_to_send += f"""
Склад: <b>{store}</b>
Тип доставки: <b>{deliv}</b>
Дней на доставку до покупателя, дни: <b>{in_days}</b>
Приоритет: <b>{prior}</b>
"""
    text_to_send += f"\nСервис также доступен на сайте: {WBCON_GEO_LINK}"
    parsing_left_count = SQL().get_parsing_left_count(user_id)
    SQL().update_parsing_left_count(user_id, parsing_left_count, 1)
    text_to_send += f"\n<i>Попыток осталось</i>: {parsing_left_count - 1}"
    return text_to_send

@dp.callback_query_handler(wb_geo.filter(action="msk"))
async def send_message(query: types.CallbackQuery, callback_data: dict):
    user_id = query.from_user.id
    data = requests.get("https://wbcon.ru/wp-admin/admin-ajax.php?action=get_result_priority&city=moscow").text
    text_to_send = create_user_text(data, user_id, "Москва")
    await bot.edit_message_text(text_to_send, user_id, query.message.message_id, parse_mode="HTML", disable_web_page_preview=True)

@dp.callback_query_handler(wb_geo.filter(action="spb"))
async def send_message(query: types.CallbackQuery, callback_data: dict):
    user_id = query.from_user.id
    data = requests.get("https://wbcon.ru/wp-admin/admin-ajax.php?action=get_result_priority&city=spb").text
    text_to_send = create_user_text(data, user_id, "Санкт-Петербург")
    await bot.edit_message_text(text_to_send, user_id, query.message.message_id, parse_mode="HTML", disable_web_page_preview=True)

@dp.callback_query_handler(wb_geo.filter(action="ekat"))
async def send_message(query: types.CallbackQuery, callback_data: dict):
    user_id = query.from_user.id
    data = requests.get("https://wbcon.ru/wp-admin/admin-ajax.php?action=get_result_priority&city=ekb").text
    text_to_send = create_user_text(data, user_id, "Екатеринбург")
    await bot.edit_message_text(text_to_send, user_id, query.message.message_id, parse_mode="HTML", disable_web_page_preview=True)

@dp.callback_query_handler(wb_geo.filter(action="habar"))
async def send_message(query: types.CallbackQuery, callback_data: dict):
    user_id = query.from_user.id
    data = requests.get("https://wbcon.ru/wp-admin/admin-ajax.php?action=get_result_priority&city=khbr").text
    text_to_send = create_user_text(data, user_id, "Хабаровск")
    await bot.edit_message_text(text_to_send, user_id, query.message.message_id, parse_mode="HTML", disable_web_page_preview=True)

@dp.callback_query_handler(wb_geo.filter(action="kazan"))
async def send_message(query: types.CallbackQuery, callback_data: dict):
    user_id = query.from_user.id
    data = requests.get("https://wbcon.ru/wp-admin/admin-ajax.php?action=get_result_priority&city=kazan").text
    text_to_send = create_user_text(data, user_id, "Казань")
    await bot.edit_message_text(text_to_send, user_id, query.message.message_id, parse_mode="HTML", disable_web_page_preview=True)

@dp.callback_query_handler(wb_geo.filter(action="belarus"))
async def send_message(query: types.CallbackQuery, callback_data: dict):
    user_id = query.from_user.id
    data = requests.get("https://wbcon.ru/wp-admin/admin-ajax.php?action=get_result_priority&city=belarus").text
    text_to_send = create_user_text(data, user_id, "Беларусь")
    await bot.edit_message_text(text_to_send, user_id, query.message.message_id, parse_mode="HTML", disable_web_page_preview=True)

@dp.callback_query_handler(wb_geo.filter(action="kazah"))
async def send_message(query: types.CallbackQuery, callback_data: dict):
    user_id = query.from_user.id
    data = requests.get("https://wbcon.ru/wp-admin/admin-ajax.php?action=get_result_priority&city=kazakh").text
    text_to_send = create_user_text(data, user_id, "Казахстан")
    await bot.edit_message_text(text_to_send, user_id, query.message.message_id, parse_mode="HTML", disable_web_page_preview=True)

@dp.callback_query_handler(wb_geo.filter(action="armenia"))
async def send_message(query: types.CallbackQuery, callback_data: dict):
    user_id = query.from_user.id
    data = requests.get("https://wbcon.ru/wp-admin/admin-ajax.php?action=get_result_priority&city=armen").text
    text_to_send = create_user_text(data, user_id, "Армения")
    await bot.edit_message_text(text_to_send, user_id, query.message.message_id, parse_mode="HTML", disable_web_page_preview=True)

@dp.callback_query_handler(wb_geo.filter(action="kirgiz"))
async def send_message(query: types.CallbackQuery, callback_data: dict):
    user_id = query.from_user.id
    data = requests.get("https://wbcon.ru/wp-admin/admin-ajax.php?action=get_result_priority&city=kirgiz").text
    text_to_send = create_user_text(data, user_id, "Киргизия")
    await bot.edit_message_text(text_to_send, user_id, query.message.message_id, parse_mode="HTML", disable_web_page_preview=True)

@dp.callback_query_handler(wb_geo.filter(action="novosib"))
async def send_message(query: types.CallbackQuery, callback_data: dict):
    user_id = query.from_user.id
    data = requests.get("https://wbcon.ru/wp-admin/admin-ajax.php?action=get_result_priority&city=novosib").text
    text_to_send = create_user_text(data, user_id, "Новосибирск")
    await bot.edit_message_text(text_to_send, user_id, query.message.message_id, parse_mode="HTML", disable_web_page_preview=True)

@dp.callback_query_handler(wb_geo.filter(action="krasnodar"))
async def send_message(query: types.CallbackQuery, callback_data: dict):
    user_id = query.from_user.id
    data = requests.get("https://wbcon.ru/wp-admin/admin-ajax.php?action=get_result_priority&city=krasnodar").text
    text_to_send = create_user_text(data, user_id, "Краснодар")
    await bot.edit_message_text(text_to_send, user_id, query.message.message_id, parse_mode="HTML", disable_web_page_preview=True)
