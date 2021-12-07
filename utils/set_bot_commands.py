from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Запустить и обновить бота"),
            types.BotCommand("parsers", "Установить парсер"),
            types.BotCommand("services", "Использовать сервисы"),
            types.BotCommand("help", "Вывести помощь"),
        ]
    )