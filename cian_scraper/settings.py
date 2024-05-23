BOT_NAME = "cian_scraper"

SPIDER_MODULES = ["cian_scraper.spiders"]
NEWSPIDER_MODULE = "cian_scraper.spiders"

ROBOTSTXT_OBEY = False
# Задержка между запросами для одного домена
DOWNLOAD_DELAY = 7
CONCURRENT_REQUESTS_PER_DOMAIN = 5
#Отключим куки
COOKIES_ENABLED = False
# Установка заголовков по умолчанию для всех запросов
DEFAULT_REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
}
# Включение AutoThrottle для автоматической настройки скорости запросов
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 10
AUTOTHROTTLE_MAX_DELAY = 60
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"


