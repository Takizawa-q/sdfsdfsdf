import logging
from loader import dp
from aiogram import executor
from utils.notify_admin import on_startup_notify
from utils.set_bot_commands import set_default_commands
import Handlers
from MySQL import SQL

logging.basicConfig(level=logging.INFO, filename="Logs/main.log", filemode="a",
                    format="%(levelname)s:%(asctime)s:%(message)s")

async def on_startup(dp):
    await on_startup_notify(dp)
    
    await set_default_commands(dp)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
