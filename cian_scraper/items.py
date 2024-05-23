# Определяем модели для элементов, которые будут собираться
import scrapy

class CianScraperItem(scrapy.Item):

    title = scrapy.Field()
    rooms = scrapy.Field()
    total_area = scrapy.Field()
    floor = scrapy.Field()
    address = scrapy.Field()
    price = scrapy.Field()
    listing_id = scrapy.Field()
    page_number = scrapy.Field()
