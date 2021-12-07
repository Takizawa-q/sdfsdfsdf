import sys
sys.path.append("c:\\Users\\xcraz\\.vscode\\TgBots")
from mysql.connector import ERROR_NO_CEXT
from MySQL import SQL
import logging
import traceback

logging.basicConfig(level=logging.DEBUG, filename="Logs/regen_tries.log", filemode="a",
                    format="%(levelname)s:%(asctime)s:%(message)s")


def main():
    user_ids: list = SQL().get_all_user_ids()
    logging.info("Regening user_parsing_left_count")
    for user_id in user_ids:
        try:
            SQL().parsing_left_count_set_200(user_id=user_id[0], amount=200)
        except Exception:
            logging.info(f"Something is wrong in regen_tries. User is - {user_id}. Error: {traceback.format_exc()}")
    logging.info("Regening user_parsing_left_count is Done!")


if __name__ == "__main__":
    main()
    
