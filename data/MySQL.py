import mysql.connector as sql
from datetime import datetime

CONFIG = {
    'host': r"149.154.64.48",  # database host
    'port': 3306,  # portid_request
    'passwd': "SWRxuT0vhLozEHCU-",
    'db': "TgBot",
    'user': "wbcon",  # username
    'charset': 'utf8',
    "autocommit": True
}


class SQL:

    def __init__(self):
        self._conn = sql.connect(**CONFIG, allow_local_infile=True)
        self._cursor = self._conn.cursor(buffered=True)

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

    def select_data_from_table(self):
        self._cursor.execute(
            f"SELECT request_id, user_id, request, is_complete, is_failed, page_start, page_finish FROM wp_ozon_user_request WHERE is_complete = 0 AND is_failed = 0 AND in_process = 0;")
        data = self._cursor.fetchall()
        return data

    def set_in_process_1(self, id):
        self._cursor.execute(
            f"UPDATE wp_ozon_user_request SET in_process = 1 WHERE (request_id = {id})")

    def set_is_failed_1(self, id):
        self._cursor.execute(
            f"UPDATE wp_ozon_user_request SET is_failed = 1 WHERE (request_id = {id})")

    def set_is_complete_1(self, id):
        self._cursor.execute(
            f"UPDATE wp_ozon_user_request SET is_complete = 1 WHERE (request_id = {id})")
        self._cursor.execute(
            f"UPDATE wp_ozon_user_request SET parsed_at = NOW() WHERE (request_id = {id})")
        self._cursor.execute(
            f"UPDATE wp_ozon_user_request SET in_process = 0 WHERE (request_id = {id})")

    def load_data_infile(self, table_from: str,
                         table_to: str):
        self._cursor.execute(
            f"LOAD DATA LOCAL INFILE '{table_from}' INTO TABLE {table_to} CHARACTER SET UTF8 FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '\"' LINES TERMINATED BY '\n' IGNORE 1 LINES (request_id, Title, Brand, BrandLink, SellerName, SellerLink, PriceDiscount, Price, Discount, DiscountPercent, Rating, Articule, DeliverySchema, ProductCount, CommentaryCount, Description, Category, ProductLink, ImageLink)")

    def select_data_from_table(self):
        self._cursor.execute(
            f"SELECT request_id, user_id, request_text FROM tg_users_requests WHERE is_complete = 0 AND is_failed = 0 and in_process = 0;")
        data = self._cursor.fetchall()
        return data

    def update_parsing_left_count(self, user_id, parsing_count):
        self._cursor.execute(
            f"UPDATE tg_users SET user_parsing_count = {parsing_count - 1} WHERE user_id = {user_id}")

    def get_data_by_request_id(self, request_id):
        return self._cursor.execute(
            "SELECT Title, Brand, BrandLink, SellerName, SellerLink,"
            "PriceDiscount, Price, Discount, DiscountPercent, Rating, Articule, DeliverySchema,"
            "ProductCount, CommentaryCount, ProductLink, ImageLink"
            f"FROM tg_users_data WHERE request_id = {request_id}").fetchone()

    def get_parsing_left_count(self, user_id):
        self._cursor.execute(
            f"SELECT user_parsing_count from tg_users WHERE user_id = {user_id}")
        return self._cursor.fetchone()

    def get_upload_data(self):
        data = self._cursor.execute(
            f"SELECT request_id, user_id, is_complete, is_failed FROM tg_users_requests WHERE is_complete = 1 AND (is_complete = 1 OR is_failed = 1)"
        )
        print(data)

    def commit(self):
        self._conn.commit()

    def __exit__(self):
        self._cursor.close()
        self._conn.commit()
