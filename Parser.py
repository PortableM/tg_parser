import requests
import re
from bs4 import BeautifulSoup


DEFAULT_PAGE = "https://t.me/s/"
OVERVIEW_PAGE = "https://t.me/"


class Parser:
    def __init__(self, channel_name, default_page=True):
        """:param default_page: страница канала если True,\
        иначе обзорная страница канала """
        self.channel_name = channel_name
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
            AppleWebKit/537.36 (KHTML, like Gecko)\
            Chrome/96.0.4664.110 Safari/537.36"
        }
        self.page_response = None
        self.domain = DEFAULT_PAGE if default_page else OVERVIEW_PAGE

    def get_name(self):
        return self.channel_name

    def parse(self):
        """Парсим страницу"""
        try:
            target_url = self.domain + self.channel_name
            page_response = requests.get(target_url, headers=self.headers)
            page_response.raise_for_status()

            self.page_response = page_response

        except requests.exceptions.RequestException as e:
            return f"Ошибка: {e}"

    def get_subscribers_count(self):
        """Возвращает количество подписчиков на канале"""
        if not hasattr(self, 'page_response'):
            return """Отсутствует ответ от канала. Вызовите метод parse\
                сначала"""

        # Определяем кол-во подписчиков
        soup = BeautifulSoup(self.page_response.content, "html.parser")
        target_element = soup.find('div', class_='tgme_page_extra')

        if target_element:
            # Вывести кол-во подписчиков
            subscribers_count = target_element.get_text()
            if subscribers_count:
                subscribers_count = re.sub(r'\D', '', subscribers_count)
                return subscribers_count
            else:
                return "Не найден текст элемента"

        else:
            return "Не найден нужный элемент"
