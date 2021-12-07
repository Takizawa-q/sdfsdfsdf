import asyncio
from SberMySQL import SBER_SQL
from MySQL import SQL
from time import sleep
from loader import bot
import logging


async def main():
    logging.basicConfig(level=logging.INFO, filename="Logs/checker.log", filemode="a",
                        format="%(levelname)s:%(asctime)s:%(message)s")
    while True:
        SBER_SQL().__exit__()
        data = SBER_SQL().get_upload_data()
        try:
            for request_id, request_text, user_id, is_complete, is_failed in data:
                if is_complete == 1 and is_failed == 0:
                    users_data = SBER_SQL().get_data_by_request_id(request_id)
                    print(users_data)
                    text_to_send = f"Результат по запросу: <b>{request_text}</b>\n"
                    text_to_send += """
<i><b>Лучший продавец:</b></i>
Заголовок: <b>{}</b>
Бренд: <b>{}</b>
Цена: <b>{}р.</b>
Наименьшая цена(у других продавцов): <b>{}р.</b>
Имя продавца: <b>{}</b>
Кол-во бонусов: <b>{}</b>
Кол-во бонусов в %: <b>{}</b>
Артикул: <b>{}</b>
Кол-во отзывов: <b>{}</b>
Кол-во товара: <b>{}</b>
Рейтинг: <b>{}</b>
                    """.format(*users_data[1:12])
                    text_to_send += f"""Изображение: <b>{users_data[18]}</b>
Ссылка на товар: <b>{users_data[-2]}</b>
"""

                    await bot.send_message(user_id, text=text_to_send, parse_mode="HTML")
                    try:
                        offs = users_data[-1].split("\n")[:-1]
                        offs = [off.split(";") for off in offs]
                        text = ""
                        for off in range(len(offs)):
                            obj = offs[off]
                            text += f"<b>{obj[0]}</b>; Цена: <b>{obj[1].replace(' ', '')}</b> Остаток: <b>{obj[2].replace(' ', '')}</b>\n"
                        offers_text_to_send = """
<i><b>Другие предложения(Название магазина; Цена; Кол-во товара)</b></i>

{}""".format(text)
                    # SBER_SQL().set_in_process_0(request_id)
                        await bot.send_message(user_id, text=offers_text_to_send, parse_mode="HTML")
                    except:
                        pass
                    try:

                        price_history_text_to_send = f"""
<i><b>История цен</b></i>\n
{users_data[-4]}"""
                        await bot.send_message(user_id, text=price_history_text_to_send, parse_mode="HTML")
                    except Exception as e:
                        print(e)
                    SBER_SQL().set_in_process_0(request_id)
                    SBER_SQL().__exit__()

                else:
                    parsing_left_count = SQL().get_parsing_left_count(user_id)
                    SQL().update_parsing_left_count(user_id, parsing_left_count, -1)
                    await bot.send_message(user_id, text=f"По вашему запросу: {request_text} не удалось получить результат, мы вернули вам попытку.")
                    logging.debug(
                        f"User didn't get the data: {user_id}, {request_id}, {request_text}")
                    SBER_SQL().set_in_process_0(request_id)
                    SQL().__exit__()
                    SBER_SQL().__exit__()

            SQL().__exit__()
            SBER_SQL().__exit__()
        except Exception as e:
            print(e)
            parsing_left_count = SQL().get_parsing_left_count(user_id)
            SQL().update_parsing_left_count(user_id, parsing_left_count, -1)
            await bot.send_message(user_id, text=f"По вашему запросу: {request_text} не удалось получить результат, мы вернули вам попытку.")
            logging.debug(
                f"User didn't get the data: {user_id}, {request_id}, {request_text}")
            SQL().__exit__()
            SBER_SQL().__exit__()
            SBER_SQL().set_in_process_0(request_id)
asyncio.run(main())
