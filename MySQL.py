import mysql.connector as sql
from datetime import datetime
import logging
import requests

CONFIG = {
    'host': r"149.154.64.48",  # database host
    'port': 3306,  # portid_request
    'passwd': "SWRxuT0vhLozEHCU-",
    'db': "TgBot",
    'user': "wbcon",  # username
    'charset': 'utf8',
    "autocommit": True
}

logging.basicConfig(level=logging.INFO, filename="Logs/MySQL.log", filemode="a",
                    format="%(levelname)s:%(asctime)s:%(message)s")


class SQL:

    def __init__(self):
        self._conn = sql.connect(**CONFIG, allow_local_infile=True)
        self._cursor = self._conn.cursor(buffered=True)

    def POST_INN_REQUEST(self, request_text, user_id):
        try:
            req = requests.get(f"http://37.46.132.15:8001/put/{user_id}?number={request_text}").json()
            return req
        except Exception as e:
            logging.info(
                f"Error occured. user_id: {user_id}. With message: {request_text}. The error is: {e}")
            return None
    
    def POST_LAMODA_REQUEST(self, request_text, user_id):
        try:
            req = requests.get(f"http://92.63.192.39:5050/put_article/arslan?q={request_text}&p=1&g=msk").text
            return req
        except Exception as e:
            logging.info(
                f"Error occured. user_id: {user_id}. With message: {request_text}. The error is: {e}")
            return None
    
    def POST_TNVED_REQUEST(self, request_text, user_id):
        try:
            req = requests.post(f"http://188.120.227.190:8084/put", data=f'{request_text}'.encode('utf-8')).json()
            return req
        except Exception as e:
            logging.info(
                f"Error occured. user_id: {user_id}. With message: {request_text}. The error is: {e}")
            return None
    
    def POST_WB_PLACE_REQUEST(self, user_id, request_text, geo, category_url, task_id):
        print(user_id, request_text, geo, category_url, task_id)
        if "%" in category_url:
            category_url = f"https://www.wildberries.ru/catalog/0/search.aspx?search={category_url}"
        print(category_url)
        try:
            requests.put(f"http://62.109.9.74/wb_art_pos_api/api/wp_art_pos_task.php", json={
    "user_id" : f"{user_id}",
    "task_id" : f"{task_id}",
    "city": f"{geo}",
    "category_url": f"{category_url}",
    "article": f"{request_text}"})
        except Exception as e:
            logging.info(
                f"Error occured. user_id: {user_id}. With message: {request_text}. The error is: {e}")
            
    def GET_WB_PLACE_REQUEST(self, user_id, task_id):
        try:
            print(user_id, task_id)
            req = requests.post(f"http://62.109.9.74/wb_art_pos_api/api/get_wp_art_pos_result.php?user_id={user_id}&task_id={task_id}")
            print(req.json())
            return req.json()
        except Exception as e:
            logging.info(
                f"Error occured. user_id: {user_id}. With message: . The error is: {e}")
            return None
    def POST_ALI_REQUEST(self, user_id, request_text):
        try:
            print(request_text)
            req = requests.get(f"http://188.120.255.121:8585/put/arslan?q={request_text}").text
            return req
        except Exception as e:
            logging.info(
                f"Error occured. user_id: {user_id}. With message: {request_text}. The error is: {e}")
            return None
    
    def POST_SBER_REQUEST(self, user_id, request_text, json_: dict):
        try:
            req = requests.post(
                f"http://149.154.64.48:8500/post_user_request/", json=json_).text
            return req
        except Exception as e:
            logging.info(
                f"Error occured. user_id: {user_id}. With message: {request_text}. The error is: {e}")
            return None
    
    def POST_WILDBERRIES_REQUEST(self, request_text, user_id):
        try:
            req = requests.get(
                f"http://92.63.192.39:5698/put/{user_id}?q={request_text}&p=1&g=msk").text
            return req
        except Exception as e:
            logging.info(
                f"Error occured. user_id: {user_id}. With message: {request_text}. The error is: {e}")
            return None
    
    def POST_KAZAN_REQUEST(self, request_text, user_id):
        try:
            req = requests.get(
                f"http://92.63.192.39:8787/put/{user_id}?q={request_text}").text
            return req
        
        except Exception as e:
            logging.info(
                f"Error occured. user_id: {user_id}. With message: {request_text}. The error is: {e}")
            return None

    def insert_into_table(self, table_name, sql_request, values):
        self._cursor.execute(f"INSERT INTO {table_name} {sql_request}", values)

    def get_req_id_status(self, req_id):
        self._cursor.execute(
            f"SELECT is_complete, is_failed, in_process FROM wp_ozon_user_request WHERE request_id = {req_id}")
        data = self._cursor.fetchall()
        return data

    def find_user_in_table(self, user_id):
        self._cursor.execute(
            f"SELECT user_id FROM tg_users WHERE user_id = {user_id}")
        data = self._cursor.fetchone()
        return data

    def create_user(self, user_id, user_username, user_first_name):
        self._cursor.execute(
            f"INSERT INTO tg_users (user_id, user_username, user_first_name) VALUES ('{user_id}', '{user_username}', '{user_first_name}')")

    def create_user_request(self, user_id, request_text):
        self._cursor.execute(
            f"INSERT INTO tg_users_requests (user_id, request_text) VALUES ('{user_id}', '{request_text}')")

    def post_wb_place_user_request(self, user_id, task_id, geo, category, article, user_got):
        self._cursor.execute(
            f"INSERT INTO tg_place_parser (user_id, task_id, geo, article, category, user_got, time_added) VALUES ('{user_id}', '{task_id}', '{geo}', '{article}', '{category}', '{user_got}', NOW())")

    def get_wb_place_user_request(self):
        self._cursor.execute(
            f"SELECT user_id, task_id, geo, category, article, time_added FROM tg_place_parser WHERE user_got = 0")
        data = self._cursor.fetchall()
        return data
    
    def select_data_from_table(self):
        self._cursor.execute(
            f"SELECT request_id, user_id, request, is_complete, is_failed, page_start, page_finish FROM wp_ozon_user_request WHERE is_complete = 0 AND is_failed = 0 AND in_process = 0;")
        data = self._cursor.fetchall()
        return data

    def set_in_process_0(self, id):
        self._cursor.execute(
            f"UPDATE tg_users_requests SET in_process = 0 WHERE (request_id = {id})")

    def set_in_process_1(self, id):
        self._cursor.execute(
            f"UPDATE tg_users_requests SET in_process = 1 WHERE (request_id = {id})")

    def load_data_infile(self, table_from: str,
                         table_to: str):
        self._cursor.execute(
            f"LOAD DATA LOCAL INFILE '{table_from}' INTO TABLE {table_to} CHARACTER SET UTF8 FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '\"' LINES TERMINATED BY '\n' IGNORE 1 LINES (request_id, Title, Brand, BrandLink, SellerName, SellerLink, PriceDiscount, Price, Discount, DiscountPercent, Rating, Articule, DeliverySchema, ProductCount, CommentaryCount, Description, Category, ProductLink, ImageLink)")

    def select_data_from_table(self):
        self._cursor.execute(
            f"SELECT request_id, user_id, request_text FROM tg_users_requests WHERE is_complete = 0 AND is_failed = 0 and in_process = 0;")
        data = self._cursor.fetchall()
        return data

    def update_parsing_left_count(self, user_id, parsing_count, amount):
        self._cursor.execute(
            f"UPDATE tg_users SET user_parsing_count = {parsing_count - amount} WHERE user_id = {user_id}")

    def set_user_got_1(self, task_id, user_id):
        self._cursor.execute(
            f"UPDATE tg_place_parser SET user_got = 1 WHERE (task_id = '{task_id}' AND user_id = '{user_id}')"
        )
    
    def get_all_user_ids(self):
        self._cursor.execute(
            f"SELECT user_id FROM tg_users WHERE user_parsing_count < 501"
        )
        data = self._cursor.fetchall()
        return list(data)
    # user_id text

    def get_all_users(self):
        self._cursor.execute(
            f"SELECT user_id, user_username, user_first_name, user_parsing_count, sm_wb, sm_ozon, sm_lamoda, sm_sber, sm_kazan, sm_ali FROM tg_users"
        )
        data = self._cursor.fetchall()
        return list(data)

    def parsing_left_count_set_200(self, user_id, amount=200):
        self._cursor.execute(
            f"UPDATE tg_users SET user_parsing_count = {amount} WHERE user_id = {user_id}")

    def set_sm_ozon_1(self, user_id):
        self._cursor.execute(
            f"UPDATE tg_users SET sm_wb = 0, sm_ozon = 1, sm_lamoda = 0, sm_sber = 0, sm_kazan = 0, sm_ali = 0, sm_inn = 0 WHERE user_id = {str(user_id)}")

    def set_sm_sber_1(self, user_id):
        self._cursor.execute(
            f"UPDATE tg_users SET sm_wb = 0, sm_ozon = 0, sm_lamoda = 0, sm_sber = 1, sm_kazan = 0, sm_ali = 0, sm_inn = 0 WHERE user_id = {str(user_id)}")

    def set_sm_wb_1(self, user_id):
        self._cursor.execute(
            f"UPDATE tg_users SET sm_wb = 1, sm_ozon = 0, sm_lamoda = 0, sm_sber = 0, sm_kazan = 0, sm_ali = 0, sm_inn = 0 WHERE user_id = {str(user_id)}"
        )

    def set_sm_tnved_1(self, user_id):
        self._cursor.execute(
            f"UPDATE tg_users SET sm_wb = 0, sm_ozon = 0, sm_lamoda = 0, sm_sber = 0, sm_kazan = 0, sm_ali = 0, sm_inn = 0 WHERE user_id = {str(user_id)}"
        )
    
    def set_sm_lamoda_1(self, user_id):
        self._cursor.execute(
            f"UPDATE tg_users SET sm_wb = 0, sm_ozon = 0, sm_lamoda = 1, sm_sber = 0, sm_kazan = 0, sm_ali = 0, sm_inn = 0 WHERE user_id = {str(user_id)}")
    
    def set_sm_inn_1(self, user_id):
        self._cursor.execute(
            f"UPDATE tg_users SET sm_wb = 0, sm_ozon = 0, sm_lamoda = 0, sm_sber = 0, sm_kazan = 0, sm_ali = 0, sm_inn = 1 WHERE user_id = {str(user_id)}")

    
    def set_sm_kazan_1(self, user_id):
        self._cursor.execute(
            f"UPDATE tg_users SET sm_wb = 0, sm_ozon = 0, sm_lamoda = 0, sm_sber = 0, sm_kazan = 1, sm_ali = 0, sm_inn = 0 WHERE user_id = {str(user_id)}")

    def set_sm_ali_1(self, user_id):
        self._cursor.execute(
            f"UPDATE tg_users SET sm_wb = 0, sm_ozon = 0, sm_lamoda = 0, sm_sber = 0, sm_kazan = 0, sm_ali = 1, sm_inn = 0 WHERE user_id = {str(user_id)}")
    
    def update_sm_ozon(self, user_id, amount):
        self._cursor.execute(
            f"UPDATE tg_users SET sm_ozon = {str(amount)} WHERE user_id = {str(user_id)}")

    def update_sm_inn(self, user_id, amount):
        self._cursor.execute(
            f"UPDATE tg_users SET sm_inn = {str(amount)} WHERE user_id = {str(user_id)}")

    
    def update_sm_wildberries(self, user_id, amount):
        self._cursor.execute(
            f"UPDATE tg_users SET sm_wb = {str(amount)} WHERE user_id = {str(user_id)}")

    def get_sm_wildberries(self, user_id):
        self._cursor.execute(
            f"SELECT sm_wb FROM tg_users WHERE user_id = {user_id}")
        data = self._cursor.fetchone()
        return int(data[0])

    def get_sm_lamoda(self, user_id):
        self._cursor.execute(
            f"SELECT sm_lamoda FROM tg_users WHERE user_id = {user_id}")
        data = self._cursor.fetchone()
        return int(data[0])
    
    def get_sm_sber(self, user_id):
        self._cursor.execute(
            f"SELECT sm_sber FROM tg_users WHERE user_id = {user_id}")
        data = self._cursor.fetchone()
        return int(data[0])
    
    def get_sm_ozon(self, user_id):
        self._cursor.execute(
            f"SELECT sm_ozon FROM tg_users WHERE user_id = {user_id}")
        data = self._cursor.fetchone()
        return int(data[0])
    
    def get_sm_inn(self, user_id):
        self._cursor.execute(
            f"SELECT sm_inn FROM tg_users WHERE user_id = {user_id}")
        data = self._cursor.fetchone()
        return int(data[0])
    
    def get_sm_ali(self, user_id):
        self._cursor.execute(
            f"SELECT sm_ali FROM tg_users WHERE user_id = {user_id}")
        data = self._cursor.fetchone()
        return int(data[0])
    
    def get_sm_kazan(self, user_id):
        self._cursor.execute(
            f"SELECT sm_kazan FROM tg_users WHERE user_id = {user_id}")
        data = self._cursor.fetchone()
        return int(data[0])

    def get_data_by_request_id(self, request_id):
        self._cursor.execute(
            f"SELECT Title, Brand, BrandLink, SellerName, SellerLink, PriceDiscount, Price, Discount, DiscountPercent, Rating, Articule, DeliverySchema, ProductCount, CommentaryCount, Credit, ProductLink, ImageLink FROM tg_users_data WHERE request_id = {request_id}")
        data = self._cursor.fetchone()
        return data

    def get_parsing_left_count(self, user_id):
        self._cursor.execute(
            f"SELECT user_parsing_count from tg_users WHERE user_id = {user_id}")
        return self._cursor.fetchone()[0]

    def get_upload_data(self):
        self._cursor.execute(
            f"SELECT request_id, request_text, user_id, is_complete, is_failed FROM tg_users_requests WHERE in_process = 1 AND (is_complete = 1 OR is_failed = 1)"
        )
        data = self._cursor.fetchall()
        return data

    def commit(self):
        self._conn.commit()

    def __exit__(self):
        self._cursor.close()
        self._conn.commit()
