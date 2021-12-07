import asyncio
from MySQL import SQL
from time import sleep
from loader import bot
import logging

from aiogram.utils.exceptions import BotBlocked


async def main():
    while True:
        logging.basicConfig(level=logging.INFO, filename="Logs/checker.log", filemode="a",
                        format="%(levelname)s:%(asctime)s:%(message)s")
        SQL().__exit__()
        data = SQL().get_upload_data()
        for request_id, request_text, user_id, is_complete, is_failed in data:
            if is_complete == 1 and is_failed == 0:
                user_data = SQL().get_data_by_request_id(request_id)
                title, brand, brand_link, seller_name, seller_link, price_discount, price, discount, discount_percent, rating, articul, deliver_schema, product_count, commentary_count, credit, product_link, image_link = user_data[::]
                text = f"""
                Результат по запросу: <b>{request_text}</b>
                Титульник: <b>{title}</b>
                Бренд: <b>{brand}</b>
                Ссылка на бренд: {brand_link}
                Имя продавца: <b>{seller_name}</b>
                Ссылка на продавца: {seller_link}
                Цена со скидкой: <b>{price_discount}</b>
                Цена без скидки: <b>{price}</b>
                Размер скидки: <b>{discount}</b>
                Скидка в %: <b>{discount_percent}</b>
                Кредит в руб/мес: <b>{credit}</b>
                Рейтинг: <b>{rating}</b>
                Артикул: <b>{articul}</b>
                Способ доставки: <b>{deliver_schema}</b>
                Кол-во остатков: <b>{product_count}</b>
                Кол-во комментариев: <b>{commentary_count}</b>
                Ссылка на картинку товара: {image_link}
                Ссылка на товар: {product_link}
    """
                try:
                    await bot.send_message(user_id, text = text, parse_mode="HTML")
                except BotBlocked:
                    pass
                print("Sended")
                SQL().set_in_process_0(request_id)
                SQL().__exit__()
            else:
                parsing_left_count = SQL().get_parsing_left_count(user_id)
                SQL().update_parsing_left_count(user_id, parsing_left_count, -1)
                await bot.send_message(user_id, text = f"По вашему запросу: {request_text} не удалось получить результат, мы вернули вам попытку.")
                logging.debug(f"User didn't get the data: {user_id}, {request_id}, {request_text}")
                SQL().set_in_process_0(request_id)
                SQL().__exit__()
        SQL().__exit__()

    
asyncio.run(main())