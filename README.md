# Cian Scraper

Этот проект предназначен для парсинга объявлений о продаже квартир на сайте Cian.ru. Используется фреймворк Scrapy и Selenium для обхода страниц и извлечения данных.

## Требования

- Python 3.8 или выше
- Scrapy
- Selenium
- Google Chrome
- ChromeDriver

## Установка

1. Клонируйте репозиторий:

    ```bash
    git clone https://github.com/User/cian_scraper.git
    cd cian_scraper
    ```

2. Создайте и активируйте виртуальное окружение:

    ```bash
    python -m venv .venv
    source .venv/bin/activate   # Для Windows: .venv\Scripts\activate
    ```

3. Установите зависимости:

    ```bash
    pip install -r requirements.txt
    ```


## Запуск

Для запуска парсера выполните следующую команду:

```bash
scrapy crawl cian -O output.json
```
Это содержит файл "output.json"

## Структука проекта 

*cian_scraper/: основной каталог проекта
  *spiders/: каталог для пауков Scrapy
     *cian_spider.py: паук для парсинга данных с сайта Cian.ru
  *items.py: определения моделей данных
  *middlewares.py: middlewares для обработки запросов и ответов
  *pipelines.py: pipelines для обработки собранных данных
  *settings.py: настройки Scrapy
*main.py: основной файл для запуска процесса парсинга

## Пример данных

```bash
{
    "heading": "1-комн. квартира, 35,83 м², 23/25 этаж",
    "rooms": "1",
    "area": "35,83",
    "floor": "23/25",
    "address": [
        "Республика Татарстан",
        "Казань",
        "р-н Советский",
        "мкр. Малые Клыки",
        "м. Горки",
        "Светлая Долина ЖК"
    ],
    "price": "7 703 450 ₽",
    "id": "300752513",
    "page_number": 1
}

```
