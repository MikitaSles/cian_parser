# Определяем модели для middleware паука
from scrapy import signals

# Полезно для обработки разных типов элементов с единым интерфейсом
from itemadapter import is_item, ItemAdapter

class CianScraperSpiderMiddleware:
    # Не все методы необходимо определять. Если метод не определен,
    # Scrapy действует так, как будто middleware паука не изменяет передаваемые объекты.
    @classmethod
    def from_crawler(cls, crawler):
        # создание паука
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Вызывается для каждого ответа, который проходит через middleware паука и попадает в паука.
        return None

    def process_spider_output(self, response, result, spider):
        # Вызывается с результатами, возвращенными пауком, после
        # обработки ответа пауком.
        # Должен возвращать итерируемый объект Request или item объектов
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        pass

    def process_start_requests(self, start_requests, spider):
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)

class CianScraperDownloaderMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        return None

    def process_response(self, request, response, spider):
        return response

    def process_exception(self, request, exception, spider):
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)
