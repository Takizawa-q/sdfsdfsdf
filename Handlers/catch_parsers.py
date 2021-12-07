from loader import dp
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from MySQL import SQL
from loader import bot
from Handlers.Parsers.ozon import parsing_cb_ozon
from Handlers.Parsers.wb import parsing_cb_wildberries
from Handlers.catch_services import services_cb
from aiogram import types
from reply_texts import WBCON_INSTRUCTION_LINK

parsing_cb = CallbackData("parsers", "action")

@dp.message_handler(lambda message: message.text == "Парсеры 🖥" or message.text == "/parsers")
async def send_message(message: types.Message):
    kb = InlineKeyboardMarkup().row(
        InlineKeyboardButton(
            "ПАРСЕР WildBerries🟣", callback_data=parsing_cb.new(action="wb"))).row(
            InlineKeyboardButton("ПОЗИЦИЯ АРТИКУЛА WILDBERRIES🟪", callback_data=services_cb.new(action="wb_place"))).row(
        InlineKeyboardButton("ПАРСЕР Ozon🔵", callback_data=parsing_cb.new(action="ozon"))).row(
            InlineKeyboardButton("ПАРСЕР Lamoda🟠", callback_data=parsing_cb.new(action="lamoda"))).row(
        InlineKeyboardButton("ПАРСЕР SberMegaMarket🟢", callback_data=parsing_cb.new(action="sber"))).row(
            InlineKeyboardButton("ПАРСЕР KazanExpress🔴", callback_data=parsing_cb.new(action="express"))).row(
        InlineKeyboardButton("ПАРСЕР Aliexpress(Tmall)🟡", callback_data=parsing_cb.new(action="ali")))
    await message.answer("Выбери необходимый тебе парсер: ", reply_markup=kb)



@dp.callback_query_handler(parsing_cb.filter(action="ali"))
async def send_message(query: types.CallbackQuery, callback_data: dict):
    user_id = query.from_user.id
    SQL().set_sm_ali_1(user_id=user_id)
    await bot.edit_message_text("Отправь артикул или ссылку на товар с Aliexpress:", user_id, query.message.message_id)

@dp.callback_query_handler(parsing_cb.filter(action="lamoda"))
async def send_message(query: types.CallbackQuery, callback_data: dict):
    user_id = query.from_user.id
    SQL().set_sm_lamoda_1(user_id=user_id)
    await bot.edit_message_text("Отправь артикул или ссылку на товар с Lamoda:", user_id, query.message.message_id)

@dp.callback_query_handler(parsing_cb.filter(action="wb"))
async def send_message(query: types.CallbackQuery, callback_data: dict):
    user_id = query.from_user.id
    SQL().set_sm_wb_1(user_id=user_id)
    await bot.edit_message_text(f"Отправь артикул или ссылку на товар с WB:\nВАЖНО!!! Обязательно прочитать разъяснения - {WBCON_INSTRUCTION_LINK}", user_id, query.message.message_id, parse_mode="HTML", disable_web_page_preview=True)

@dp.callback_query_handler(parsing_cb.filter(action="ozon"))
async def send_message(query: types.CallbackQuery, callback_data: dict):
    user_id = query.from_user.id
    SQL().set_sm_ozon_1(user_id=user_id)
    await bot.edit_message_text("Отправь артикул или ссылку на товар с Ozon:", user_id, query.message.message_id)
    
@dp.callback_query_handler(parsing_cb.filter(action="sber"))
async def send_message(query: types.CallbackQuery, callback_data: dict):
    user_id = query.from_user.id
    SQL().set_sm_sber_1(user_id=user_id)
    await bot.edit_message_text("Отправь артикул или ссылку на товар с СберМегаМаркет:", user_id, query.message.message_id)

@dp.callback_query_handler(parsing_cb.filter(action="express"))
async def send_message(query: types.CallbackQuery, callback_data: dict):
    user_id = query.from_user.id
    SQL().set_sm_kazan_1(user_id=user_id)
    await bot.edit_message_text("Отправь артикул или ссылку на товар с Казань Экспресс:", user_id, query.message.message_id)




