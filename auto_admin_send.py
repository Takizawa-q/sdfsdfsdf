from data.config import ADMINS
from MySQL import SQL
from loader import bot
import asyncio
import xlsxwriter
async def main():
    data = SQL().get_all_users()
    workbook = xlsxwriter.Workbook('UsersData.xls')
    worksheet = workbook.add_worksheet()
    row = 0
    col = 0
    ozon_user_count = 0
    wb_user_count = 0
    lamoda_user_count = 0
    sber_user_count = 0
    kazan_user_count = 0
    ali_user_count = 0
    max_tries_count = []
    summ_tries_count = 0
    for i in ["id Пользователя", "Никнейм", "Имя", "Попыток использовано", "Последний парсер"]:
        worksheet.write(row, col, i)
        col += 1
    
    row = 1
    for user_id, user_username, user_first_name, tries_count, sm_wb, sm_ozon, sm_lamoda, sm_sber, sm_kazan, sm_ali in data:
        col = 0
        last_used_parser = ""
        if sm_wb == 1:
            last_used_parser += "WB"
            wb_user_count += 1
        elif sm_ozon == 1:
            last_used_parser += "Ozon"
            ozon_user_count += 1
        elif sm_lamoda == 1:
            last_used_parser += "lamoda"
            lamoda_user_count += 1
        elif sm_sber == 1:
            last_used_parser += "Sber"
            sber_user_count += 1
        elif sm_kazan == 1:
            last_used_parser += "Kazan"
            kazan_user_count += 1
        elif sm_ali == 1:
            last_used_parser += "Ali"
            ali_user_count += 1
        
        used_tries_count = 200 - int(tries_count)
        summ_tries_count += used_tries_count
        max_tries_count.append(used_tries_count)
        
        for i in [str(user_id), user_username, user_first_name, used_tries_count, last_used_parser]:
            worksheet.write(row, col, i)
            col += 1
        row += 1
    
    worksheet.write(0, 6, "Использующих WB")
    worksheet.write(1, 6, wb_user_count)
    worksheet.write(0, 7, "Использующих Ozon")
    worksheet.write(1, 7, ozon_user_count)
    worksheet.write(0, 8, "Использующих Lamoda")
    worksheet.write(1, 8, lamoda_user_count)
    worksheet.write(0, 9, "Использующих Sber")
    worksheet.write(1, 9, sber_user_count)
    worksheet.write(0, 10, "Использующих Kazan")
    worksheet.write(1, 10, kazan_user_count)
    worksheet.write(0, 11, "Использующих Aliexpress")
    worksheet.write(1, 11, ali_user_count)
    worksheet.write(2, 6, "Использовано попыток всего")
    worksheet.write(3, 6, summ_tries_count)
    worksheet.write(2, 7, "Макс попыток одним пользователем")
    worksheet.write(3, 7, max(max_tries_count))
    workbook.close()
    file = open("UsersData.xls", "rb")
    for admin in ADMINS:
        await bot.send_document(admin, file)

if __name__ == "__main__":
    asyncio.run(main())