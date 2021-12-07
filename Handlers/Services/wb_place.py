from time import sleep
from operator import itemgetter
from ast import literal_eval
from datetime import date
import string
import random
from aiogram.dispatcher.storage import FSMContext
from MySQL import SQL
from aiogram.utils.callback_data import CallbackData
from datetime import datetime
from loader import bot, dp
from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from reply_texts import WBCON_LINK, WBCON_STORAGES_LINK
from Handlers.catch_services import services_cb
from aiogram.dispatcher.filters.state import StatesGroup, State

geo_cb = CallbackData("geo", "action")


class Place(StatesGroup):
    geo = State()
    category = State()
    article = State()


@dp.callback_query_handler(services_cb.filter(action="wb_place"))
async def enter_geo(query: types.CallbackQuery, callback_data: dict):
    user_id = query.from_user.id
    if SQL().get_parsing_left_count(user_id) > 0:
        user_id = query.from_user.id
        kb = InlineKeyboardMarkup().row(
            InlineKeyboardButton("Москва", callback_data=geo_cb.new(action="moscow"))).row(
            InlineKeyboardButton("Санкт-Петербург", callback_data=geo_cb.new(action="spb"))).row(
            InlineKeyboardButton("Казань", callback_data=geo_cb.new(action="kazan"))).row(
            InlineKeyboardButton("Хабаровск", callback_data=geo_cb.new(action="khbr"))).row(
            InlineKeyboardButton("Краснодар", callback_data=geo_cb.new(action="krasnodar"))).row(
            InlineKeyboardButton("Новосибирск", callback_data=geo_cb.new(action="novosib"))).row(
            InlineKeyboardButton("Отменить", callback_data=geo_cb.new(action="mega_cancel")))
        await bot.edit_message_text("Выбери гео поиска:", user_id, query.message.message_id, reply_markup=kb)
        await Place.geo.set()
    else:
        await bot.send_message(user_id, "Извини, но у тебя закончились попытки😔 Советуем посетить наш сайт <b>{WBCON_LINK}</b>, где вы сможете купить безлимитную версию парсера, которая может парсить не только артикулы, но и категории, поисковые запросы, бренды и поставщиков!\nhttps://wbcon.ru/parser-ozon/",
                                    parse_mode="HTML")
 
@dp.callback_query_handler(geo_cb.filter(action="mega_cancel"), state="*")
async def send_Message(query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    user_id = query.from_user.id
    await bot.edit_message_text("Отменено!", user_id, query.message.message_id)
    await state.finish()

@dp.callback_query_handler(geo_cb.filter(action=["moscow", "spb", "kazan", "khbr", "krasnodar", "novosib"]), state=Place.geo)
async def send_Message(query: types.CallbackQuery, callback_data: dict, state):
    geo = callback_data["action"]
    kb = InlineKeyboardMarkup().row(InlineKeyboardButton("Отменить", callback_data=geo_cb.new(action="mega_cancel")))
    await bot.edit_message_text("Отправь артикул искомого товара:", query.from_user.id, query.message.message_id, reply_markup=kb)
    async with state.proxy() as data:
        data["geo"] = geo
    await Place.next()


@dp.message_handler(state=Place.category)
async def send_message(message: types.Message, state: FSMContext):
    kb = InlineKeyboardMarkup().row(InlineKeyboardButton("Отменить", callback_data=geo_cb.new(action="mega_cancel")))
    await message.answer("Отправь категорию, в которой нужно найти этот артикул:", reply_markup=kb)
    async with state.proxy() as data:
        data["category"] = message.text
    await Place.next()


@dp.message_handler(state=Place.article)
async def send_message(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    async with state.proxy() as data:
        data["article"] = message.text
    parsing_left_count = SQL().get_parsing_left_count(user_id)
    SQL().update_parsing_left_count(user_id, parsing_left_count, 1)
    await message.answer(f"Дожидайтесь результата, скоро он будет отправлен.\n<i>Попыток осталось: {parsing_left_count - 1}</i>", parse_mode="HTML")
    await parse_state(message, state)


async def parse_state(message: types.Message, state: FSMContext):
    data = await state.get_data()
    geo, category, article = data["geo"], data["category"], data["article"]
    user_id = message.from_user.id
    print(article)
    if article.replace(" ", "").isalpha():
        text_1 = bytes(article, encoding="UTF-8")
        article = str(text_1)[2:-1].replace("x", "").replace("d", "D").replace("a", "A").replace("b", "B").replace("c",
                                                                                                                  "C").replace(
            "e", "E").replace("f", "F").replace('\\', "%").replace(" ", "+")
    await state.finish()
    task_id = string.ascii_uppercase + string.ascii_lowercase + string.digits
    task_id = ''.join(random.choice(task_id) for _ in range(10))
    SQL().post_wb_place_user_request(user_id, task_id, geo, article, category, user_got=0)
    SQL().POST_WB_PLACE_REQUEST(user_id, category, geo, article, task_id)

