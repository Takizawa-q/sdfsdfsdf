import sys

from aiogram.utils.markdown import text
sys.path.append("c:\\Users\\xcraz\\.vscode\\TgBots")
import asyncio
import traceback
from urllib.parse import unquote
from datetime import datetime
import json
from loader import bot
from multiprocessing import Pool
from reply_texts import WBCON_WB_PLACE_LINK
from time import sleep
import logging
import sys
from MySQL import SQL

async def main():
    while True:
        logging.basicConfig(level=logging.INFO, filename="Logs/checker.log", filemode="a",
                        format="%(levelname)s:%(asctime)s:%(message)s")
        SQL().__exit__()
        data = SQL().get_wb_place_user_request()
        for user_id, task_id, geo, category, article, time_added  in data:
            delta = datetime.now() - time_added
            if delta.total_seconds() > 5:
                try:
                    data = SQL().GET_WB_PLACE_REQUEST(user_id, task_id)

                    status_message = data["message"]
                    data = json.loads(data["data"])
                    if status_message == "Error":
                        raise Exception
                    if data["position"] == "-1":
                        raise KeyError
                    if category.startswith("http"):
                        category_print = category
                    else:
                        category_print = unquote(category)
                    print(category_print)
                    cities_dict = {"moscow": "Москва", "spb": "Санкт-Петербург", "kazan": "Казань", "khbr": "Хабаровск", "krasnodar": "Краснодар", "novosib": "Новосибирск"}        
                    text_to_send = f"Ваш результат по поиску места артикула: <b>{article}</b>\nВ категории: <b>{category_print}</b>\n"
                    text_to_send += f"Геолокация: <b>{cities_dict[geo]}</b>\n"
                    text_to_send += f"Место товара: <b>{data['position']}</b>\n"
                    text_to_send += f"Поставить на мониторинг позиций товар Вы можете в сервисе {WBCON_WB_PLACE_LINK}"

                    await bot.send_message(user_id, text = text_to_send, parse_mode="HTML", disable_web_page_preview=True)
                    SQL().set_user_got_1(task_id, user_id)
                    
                except KeyError:
                    await bot.send_message(user_id, text = f"Просим прощения, но, видимо, данного товара: {article}, нет в: https://www.wildberries.ru/catalog/0/search.aspx?search={category}", parse_mode="HTML", disable_web_page_preview=True)
                    parsing_count = SQL().get_parsing_left_count(user_id)
                    SQL().set_user_got_1(task_id, user_id)
                    SQL().update_parsing_left_count(user_id, parsing_count, -1)
                except Exception as e:
                    print(traceback.format_exc())
                    parsing_count = SQL().get_parsing_left_count(user_id)
                    SQL().set_user_got_1(task_id, user_id)
                    SQL().update_parsing_left_count(user_id, parsing_count, -1)
                    await bot.send_message(user_id, text = f"Просим прощения, но по твоему запросу: <b>{article}</b> не удалось ничего найти😔 Но мы вернули тебе попытку!", parse_mode="HTML", disable_web_page_preview=True)
            else:
                pass
            SQL().__exit__()
 
asyncio.run(main())