import scrapy
from scrapy import Selector
from scrapy.exceptions import CloseSpider
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
from urllib.parse import urlparse, parse_qs
from cian_scraper.items import CianScraperItem

class CianSpider(scrapy.Spider):
    name = "cian"
    start_urls = [
        "https://kazan.cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=flat&p=1&region=4777&room1=1"
    ]

    current_url = 'https://kazan.cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=flat&p=1&region=4777&room1=1'

    # Выводим результаты в формате JSON
    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': 'cavalerki.json'
    }
    prev_page_number = 0

    def __init__(self, *args, **kwargs):
        super(CianSpider, self).__init__(*args, **kwargs)
        # веб-драйвера Chrome для Selenium
        self.driver = webdriver.Chrome()

    def parse(self, response):
        ROOM_INDEX = 0
        AREA_INDEX = 2
        FLOOR_INDEX = 4
        ID_INDEX = -2
        ALLOWED_VALUES = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

        # Получаем текущий номер страницы из URL
        # Если номера страницы нет в URL даём 1
        try:
            page_number = int(response.url.split('&p=')[1].split('&')[0])
        except IndexError:
            page_number = 1

        # Проверяем, если текущий номер страницы больше или равен предыдущему
        if page_number >= self.prev_page_number:
            self.prev_page_number = page_number
        else:
            # Если номер страницы меньше, вызываем исключение и останавливаем работу программы
            raise CloseSpider("Достигнут предел страниц")

        # Проверяем наличие контейнера с доп предложениями на странице
        additional_block = response.xpath('//div[@data-name="Suggestions"]')
        if len(additional_block) != 0:
            response = self.click_more_button()
        # Обработка блока объявлений
        for offers in response.css('div._93444fe79c--general--BCXJ4'):
            heading_text = offers.css(
                'span[data-mark="OfferTitle"] span::text'
            ).get()
            if not heading_text:
                continue
            if list(heading_text.split()[0])[0] not in ALLOWED_VALUES:
                continue

            heading_parts = heading_text.split()
            if len(heading_parts) < 5:
                continue

            rooms_values = list(heading_parts[ROOM_INDEX])
            rooms = ''
            for value in rooms_values:
                try:
                    int_value = int(value)
                    rooms += str(int_value)
                except ValueError:
                    break


            # Удалим пробелы из цены
            price = offers.css('span[data-mark="MainPrice"] span::text').get()
            price = price.replace('\xa0', '')
            # Сборка
            ad_data = {
                'heading': heading_text,
                'rooms': rooms,
                'area': heading_parts[AREA_INDEX],
                'floor': heading_parts[FLOOR_INDEX],
                'address': offers.css('a[data-name="GeoLabel"]::text').getall(),
                'price': price,
                'id': str(offers.css('a._93444fe79c--link--VtWj6').attrib['href']).split('/')[ID_INDEX],
                'page_number': page_number,
            }
            yield ad_data

        # Переход на следующую страницу
        self.current_url = self.current_url.replace(f"p={page_number}", f"p={page_number + 1}")
        if self.current_url is not None:
            yield response.follow(self.current_url, self.parse)



    def click_more_button(self) -> HtmlResponse:
        # Открыть текущую страницу
        self.driver.get(self.current_url)

        # Задержка на подгрузку
        time.sleep(5)

        # Проверяем на плашку принятия куки
        try:
            accept_cookies_button = self.driver.find_element(By.XPATH, "//div[@data-name='CookiesNotification']//div[@class='_25d45facb5--button--CaFmg']")
            accept_cookies_button.click()
            time.sleep(2)
        except NoSuchElementException:
            pass
        # Нажимаем "Показать ещё"
        while True:
            try:
                more_button = self.driver.find_element(By.CLASS_NAME, '_93444fe79c--moreSuggestionsButtonContainer--h0z5t')
                more_button.click()
                time.sleep(5)
            except:
                break

        # Обновляем содержимое ответа Scrapy
        body = self.driver.page_source
        url = self.driver.current_url
        response = HtmlResponse(url=url, body=body, encoding='utf-8')
        return response

    def closed(self, reason):
        # Закрытие веб-драйвера при завершении работы паука
        self.driver.quit()
        self.log(f"Spider closed: {reason}")
