from time import sleep
import re
import json
from ast import literal_eval
import requests
from datetime import date
from MySQL import SQL
from Handlers.Parsers.ozon import ozon_send_message
from loader import bot, dp
from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from reply_texts import WBCON_LINK, WBCON_STORAGES_LINK

parsing_cb_wildberries = CallbackData('parsing_wb', 'action')


async def wb_send_message(message: types.Message):
    user_id = message.from_user.id
    print(user_id)
    parsing_left_count = SQL().get_parsing_left_count(user_id)
    if parsing_left_count > 0:
        message_text = message.text
        await message.answer(f"Ждите результат, скоро он придёт в чат сообщением(WB в порядке очереди).\nОсталось попыток: {parsing_left_count - 1} из 200 на сегодняшний день",)

        SQL().update_parsing_left_count(user_id, parsing_left_count, amount=1)
        if message_text.isdigit():
            pass
        else:
            message_text = re.search(
                "https://(www\.|)wildberries\.ru/catalog/(\d*)", str(message_text)).group(2)
        ud = SQL().POST_WILDBERRIES_REQUEST(message_text, user_id)
        try:
            ud = json.loads(ud)
            podolsk, podolsk_total = ud["wh_117501"], ud["wh_117501_sum"]
            coledino, coledino_total = ud["wh_507"], ud["wh_507_sum"]
            novosib, novosib_total = ud["wh_686"], ud["wh_686_sum"]
            habarovsk, habarovsk_total = ud["wh_1193"], ud["wh_1193_sum"]
            krasnodar_old, krasnodar_old_total = ud["wh_1699"], ud["wh_1699_sum"]
            krasnodar, krasnodar_total = ud["wh_130744"], ud["wh_130744_sum"]
            ekaterinburg, ekaterinburg_total = ud["wh_1733"], ud["wh_1733_sum"]
            piter, piter_total = ud["wh_2737"], ud["wh_2737_sum"]
            kazan, kazan_total = ud["wh_117986"], ud["wh_117986_sum"]
            domodedovo, domodedovo_total = ud["wh_116433"], ud["wh_116433_sum"]
            fbs, fbs_total = ud["wh_fbs"], ud["wh_fbs_sum"]
            elektrostal, elektrostal_total = ud["wh_120762"], ud["wh_120762_sum"]
            elektrostal_kbt, elektrostal_kbt_total = ud["wh_120602"], ud["wh_120602_sum"]
            elektrostal_kbt_2, elektrostal_kbt_2_total = ud["wh_121709"], ud["wh_121709_sum"]
            ostatok = ud["all_qty"]
            storage_text_to_send = "<i>ОСТАТКИ ПО СКЛАДАМ</i>:\n"
            if podolsk is not None:
                storage_text_to_send += f"Подольск: <b>{podolsk}</b>" + "\n"
            if podolsk_total is not None:
                storage_text_to_send += f"Подольск всего: <b>{podolsk}</b>" + "\n"
            if coledino is not None:
                storage_text_to_send += f"Коледино: <b>{coledino}</b>" + "\n"
            if coledino_total is not None:
                storage_text_to_send += f"Коледино всего: <b>{coledino_total}</b>" + "\n"
            if novosib is not None:
                storage_text_to_send += f"Новосибирск: <b>{novosib}</b>" + "\n"
            if novosib_total is not None:
                storage_text_to_send += f"Новосибирск всего: <b>{novosib_total}</b>" + "\n"
            if krasnodar_old is not None:
                storage_text_to_send += f"Краснодар-старый: <b>{krasnodar_old}</b>" + "\n"
            if krasnodar_old_total is not None:
                storage_text_to_send += f"Краснодар-старый всего: <b>{krasnodar_old_total}</b>" + "\n"
            if habarovsk is not None:
                storage_text_to_send += f"Хабаровск: <b>{habarovsk}</b>" + "\n"
            if habarovsk_total is not None:
                storage_text_to_send += f"Хабаровск всего: <b>{habarovsk_total}</b>" + "\n"
            if krasnodar is not None:
                storage_text_to_send += f"Краснодар: <b>{krasnodar}</b>" + "\n"
            if krasnodar_total is not None:
                storage_text_to_send += f"Краснодар всего: <b>{krasnodar_total}</b>" + "\n"
            if ekaterinburg is not None:
                storage_text_to_send += f"Екатеринбург: <b>{ekaterinburg}</b>" + "\n"
            if ekaterinburg_total is not None:
                storage_text_to_send += f"Екатеринбург всего: <b>{ekaterinburg_total}</b>" + "\n"
            if piter is not None:
                storage_text_to_send += f"Питер: <b>{piter}</b>" + "\n"
            if piter_total is not None:
                storage_text_to_send += f"Питер всего: <b>{piter_total}</b>" + "\n"
            if kazan is not None:
                storage_text_to_send += f"Казань: <b>{kazan}</b>" + "\n"
            if kazan_total is not None:
                storage_text_to_send += f"Казань всего: <b>{kazan_total}</b>" + "\n"
            if domodedovo is not None:
                storage_text_to_send += f"Домодедово: <b>{domodedovo}</b>" + "\n"
            if domodedovo_total is not None:
                storage_text_to_send += f"Домодедово всего: <b>{domodedovo_total}</b>" + "\n"
            if fbs is not None:
                storage_text_to_send += f"FBS: <b>{fbs}</b>" + "\n"
            if fbs_total is not None:
                storage_text_to_send += f"FBS всего: <b>{fbs_total}</b>" + "\n"
            if elektrostal is not None:
                storage_text_to_send += f"Электросталь: <b>{elektrostal}</b>" + "\n"
            if elektrostal_total is not None:
                storage_text_to_send += f"Электросталь всего:<b>{elektrostal_total}</b>" + "\n"
            if elektrostal_kbt is not None:
                storage_text_to_send += f"Электросталь-КБТ: <b>{elektrostal_kbt}</b>" + "\n"
            if elektrostal_kbt_total is not None:
                storage_text_to_send += f"Электросталь-КБТ всего: <b>{elektrostal_kbt_total}</b>" + "\n"
            if elektrostal_kbt_2 is not None:
                storage_text_to_send += f"Электросталь-КБТ-2: <b>{elektrostal_kbt_2}</b>" + "\n"
            if elektrostal_kbt_2_total is not None:
                storage_text_to_send += f"Электросталь-КБТ-2 всего: <b>{elektrostal_kbt_2_total}</b>" + "\n"
            storage_text_to_send += f"Общий остаток: <b>{ostatok}</b>"
            try:
                discount = round(
                    (1 - (int(ud["item_price_with_sale"]) / int(ud["basic_price"]))) * 100, 1)
            except:
                discount = 0
            try:
                y, m, d = map(int, str(ud["first_feedback_date"]).split("-"))
                first_feedback = date(y, m, d)
                days_passed = int((date.today() - first_feedback).days)
                vel_of_buying_xxx = round(int(ud['orders_count']) / days_passed, 2)
                
                vel_of_buying_yyy = int(ud["item_price_with_sale"]) * vel_of_buying_xxx
                print(vel_of_buying_xxx, type(vel_of_buying_xxx), vel_of_buying_yyy, type(vel_of_buying_yyy))
            except:
                pass
            print(ud)
            text_to_send = f"""
Результат по запросу: <b>{message_text}</b>
Название: <b>{ud["item_name"]}</b>
Артикул: <b>{ud["item_id"]}</b>
Бренд: <b>{ud["brand_name"]}</b>
Рейтинг: <b>{ud["rating_avg"]}</b>
Кол-во отзывов: <b>{str(ud["feedbacks"]).replace("-", "")}</b>
Дата первого отзыва: <b>{ud["first_feedback_date"]}</b>
Цена до скидки: <b>{ud["basic_price"]}</b>
Цена со скидкой: <b>{ud["item_price_with_sale"]}</b>
Скидка в %: <b>{ud["basic_sale"]}</b>
Скидка по промокоду в %: <b>{ud["promo_sale"]}</b>
Имя продавца: <b>{ud["supplier_name"]}</b>
ОГРН: <b>{ud["ogrn"]}</b>
ИНН: <b>{ud["inn"]}</b>
Юридический адрес: <b>{ud["legal_address"]}</b>
Страна изготовитель: <b>{ud["country_"]}</b>
Цвет: <b>{ud["colorname"]}</b>
Комплектация: <b>{ud["complectation"]}</b>
Описание: <b>{ud["description"]}</b>
Ссылка на продавца: <b>{ud["supplier_url"]}</b>
Ссылка на товар: <b>{ud["item_url"][:-1]}</b>
            """
            storage_text_to_send += f"\nКол-во выкупов: <b>{ud['orders_count']}</b>"
            try:
                storage_text_to_send += f"\nСредняя скорость выкупа(за весь период): <b>{str(round(vel_of_buying_xxx, 3))}</b> ед./дн. и <b>{str(round(vel_of_buying_yyy, 3))}</b> руб./дн."
            except:
                pass
            try:
                storage_text_to_send += f"\nВыручка за весь период: <b>{round(int(ud['orders_count']) * int(ud['item_price_with_sale']), 3)}</b> руб."
            except:
                pass
            await message.answer(text_to_send, parse_mode="HTML")
            await message.answer(storage_text_to_send, parse_mode="HTML")
        except Exception as e:
            await message.answer(f"Просим прощения, но по твоему запросу не удалось ничего найти😔 Но мы вернули тебе попытку!")
            print(e)
            parsing_count = SQL().get_parsing_left_count(user_id)
            SQL().update_parsing_left_count(user_id, parsing_count, -1)
    else:
        await message.answer(f"Извини, но у тебя закончились попытки😔 Советуем посетить наш сайт <b>{WBCON_LINK}</b>, где вы сможете купить безлимитную версию парсера, которая может парсить не только артикулы, но и категории, поисковые запросы, бренды и поставщиков!\nhttps://wbcon.ru/",
                                    parse_mode="HTML")