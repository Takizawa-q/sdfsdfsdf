import mysql.connector as sql
from datetime import datetime
import logging
import requests

CONFIG = {
    'host': r"149.154.64.48",  # database host
    'port': 3306,  # portid_request
    'passwd': "SWRxuT0vhLozEHCU-",
    'db': "SberMega",
    'user': "wbcon",  # username
    'charset': 'utf8',
    "autocommit": True
}


class SBER_SQL:

    def __init__(self):
        self._conn = sql.connect(**CONFIG, allow_local_infile=True)
        self._cursor = self._conn.cursor(buffered=True)

    def get_upload_data(self):
        self._cursor.execute(
            f"SELECT request_id, request, user_id, is_complete, is_failed FROM wp_sber_user_request WHERE in_process = 1 AND (is_complete = 1 OR is_failed = 1)"
        )
        data = self._cursor.fetchall()
        return data

    def set_in_process_0(self, id):
        self._cursor.execute(
            f"UPDATE wp_sber_user_request SET in_process = 0 WHERE (request_id = {id})")

    def get_data_by_request_id(self, request_id):
        self._cursor.execute(
            f"SELECT * FROM wp_sber_data WHERE request_id = {request_id}")
        data = self._cursor.fetchone()
        return data

    def __exit__(self):
        self._cursor.close()
        self._conn.commit()
