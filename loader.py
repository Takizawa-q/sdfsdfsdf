from aiogram import Bot, Dispatcher
from data import API_TOKEN, TEST_API_TOKEN
from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot = Bot(token=TEST_API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())