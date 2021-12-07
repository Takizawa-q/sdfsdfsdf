from aiogram import types
from MySQL import SQL
import logging
from Buttons.button_combinations import MAIN_MENU_BUTTON
from reply_texts import WBCON_LINK
from loader import dp


logging.basicConfig(level=logging.INFO, filename="Logs/main.log", filemode="a",
            format="%(levelname)s:%(asctime)s:%(message)s")

@dp.message_handler(lambda message: message.text == "/start")
async def send_welcome_message(message: types.Message):
    user_username = message.from_user.username
    user_first_name = message.from_user.first_name
    user_id = SQL().find_user_in_table(message.from_user.id)
    
    if not user_id:
        SQL().create_user(message.from_user.id, user_username, user_first_name)
        logging.info(
            f"Пользователь создан: {str(message.from_user.id)}, {user_username}")
    else:
        SQL().update_sm_wildberries(user_id[0], 0)
        SQL().update_sm_ozon(user_id[0], 0)
    parsing_left_count = SQL().get_parsing_left_count(message.from_user.id)
    await message.answer(f"➖➖➖➖➖➖➖➖➖\nВаш профиль:\n    🆔 Ваш id: {message.from_user.id}\n    👤 Ваше имя: {user_first_name}\n    🤖 Ваш юзернейм: {user_username}\n    💻Попыток для парсинга осталось: {parsing_left_count}\n➖➖➖➖➖➖➖➖➖")

    await message.answer(f"Добро пожаловать в Telegram бота от команды 🟣{WBCON_LINK}🟣!\nЧтобы начать работу с ботом просто нажми на интересующий тебя МП ниже⬇️",
                         reply_markup=MAIN_MENU_BUTTON,
                         parse_mode="HTML",
                         disable_web_page_preview=True)