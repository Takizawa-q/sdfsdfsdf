from aiogram import types
from loader import dp, bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from MySQL import SQL

services_cb = CallbackData("services", "action")

@dp.message_handler(lambda message: message.text == "Сервисы 💻" or message.text == "/services")
async def send_message(message: types.Message):
    kb = InlineKeyboardMarkup().row(
        InlineKeyboardButton(
            "ЛИМИТЫ СКЛАДОВ WB🟣", callback_data=services_cb.new(action="wb_storages"))).row(InlineKeyboardButton(
                "КОЭФФИЦИЕНТ ГЕО WILDBERRIES🟣", callback_data=services_cb.new(action="wb_geo"))).row(
            InlineKeyboardButton("ПОДБОР ТН ВЭД⚫️", callback_data=services_cb.new(action="tnved"))).row(
                InlineKeyboardButton("ПАРСЕР ИНН/ОГРН⚫️", callback_data=services_cb.new(action="inn"))).row(
        InlineKeyboardButton("Больше сервисов в дальнейшем...", callback_data=services_cb.new(action="test")))
    await message.answer("Выбери необходимый тебе сервис: ", reply_markup=kb)



