from aiogram.utils.markdown import hlink


WBCON_LINK = hlink('WbCon', 'https://wbcon.ru/')
WBCON_STORAGES_LINK = hlink('WbCon', 'https://wbcon.ru/proverka-limitov-wildberries/')
WBCON_GEO_LINK = hlink('WbCon', 'https://wbcon.ru/geo-wb-sklad/')
WBCON_BOT_HELP_LINK = hlink('WbCon', "https://wbcon.ru/2021/10/31/bot-parser-mp-telegram/")
WBCON_WB_PLACE_LINK = hlink('Мониторинг позиций на WBCON', "https://wbcon.ru/monitoring-pozicii-wb/")
WBCON_INSTRUCTION_LINK = hlink('ЗДЕСЬ', 'https://wbcon.ru/2021/10/31/bot-parser-mp-telegram/')
cities_dict = {"moscow": "Москва", "spb": "Санкт-Петербург", "kazan": "Казань", "khbr": "Хабаровск", "krasnodar": "Краснодар", "novosib": "Новосибирск"}        
help_text = f"""<i>Инструкция по использованию бота:
1) Нажми на кнопку Парсеры или Сервисы, чтобы посмотреть, какие услуги мы предлагаем.
2) Нажми на кнопку(отправленную ботом) с нужной тебе услугой.
3) Отправь в чат то, что надо спарсить. Парсить можно ТОЛЬКО артикулы(по номеру артикула) или ссылки на товар.
4) Бот помнит последний выбранный парсер, поэтому проделывать пункты 1 и 2 не обязательно, только, если вы не хотите сменить парсер.
Подробная инструкция по боту - {WBCON_BOT_HELP_LINK}
Полноценный парсинг: парсинг артикулов, поисковых запросов, категорий, продавцов, брендов доступен на сайте {WBCON_LINK}</i>"""
