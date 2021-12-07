from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types.inline_keyboard import InlineKeyboardButton
from loader import dp, bot
from aiogram.utils.callback_data import CallbackData
import json
class LimitState(StatesGroup):
    storage = State()
    type_send = State()
    limit = State()

cb_data = CallbackData("types", "action")

@dp.message_handler(lambda message: message.text == "Отслеживание лимитов складов WB🟣", state=None)
async def send_message(message: types.Message):
    kb = InlineKeyboardMarkup().row(
        InlineKeyboardButton(
            "Подольск", callback_data=cb_data.new(action="Podolsk"))
    ).row(InlineKeyboardButton("Коледино", callback_data=cb_data.new(action="Koledino"))).row(
        InlineKeyboardButton(
            "Электросталь", callback_data=cb_data.new(action="Elektro"))
    ).row(InlineKeyboardButton("Электросталь КБТ", callback_data=cb_data.new(action="ElektroKBT"))).row(
        InlineKeyboardButton(
            "Санкт-Петербург", callback_data=cb_data.new(action="Piter"))
    ).row(InlineKeyboardButton("Екатеринбург", callback_data=cb_data.new(action="Ekat"))).row(
        InlineKeyboardButton(
            "Новосибирск", callback_data=cb_data.new(action="Novosib"))
    ).row(InlineKeyboardButton("Краснодар", callback_data=cb_data.new(action="Krasnodar"))).row(
        InlineKeyboardButton(
            "Хабаровск", callback_data=cb_data.new(action="Habarovsk"))
    ).row(InlineKeyboardButton("Казань", callback_data=cb_data.new(action="Kazan")))
    await LimitState.storage.set()
    await message.answer("Выберите склад:", reply_markup=kb)
    
@dp.callback_query_handler(cb_data.filter(action=["Podolsk", "Koledino", "Elektro", "ElektroKBT", "Piter", "Ekat", "Novosib", "Krasnodar", "Habarovsk", "Kazan"]))
async def send_message(query: types.CallbackQuery, callback_data: dict):
    dat = query.data
    stor_name = ""
    for val in json.loads(query.as_json())["message"]["reply_markup"]["inline_keyboard"]:
        val = val[0]
        if val["callback_data"] == dat:
            stor_name += val["text"]
    
    await bot.edit_message_text("123123")