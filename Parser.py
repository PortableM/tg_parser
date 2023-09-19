import requests
from bs4 import BeautifulSoup


DOMAIN = "https://t.me/s/"


class Parser:
    def __init__(self, channel_name):
        self.channel_name = channel_name
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
        }
        self.page_response = None

    def get_name(self):
        return self.channel_name

    def parse(self):
        """Парсим канал"""
        try:
            target_url = DOMAIN + self.channel_name
            page_response = requests.get(target_url, headers=self.headers)
            page_response.raise_for_status()

            self.page_response = page_response

        except requests.exceptions.RequestException as e:
            return f"Ошибка: {e}"

    def get_subscribers_count(self):
        """Возвращает количество подписчиков на канале"""
        if not hasattr(self, 'page_response'):
            return """Отсутствует ответ от канала. Вызовите метод parse сначала"""

        # Определяем кол-во подписчиков
        soup = BeautifulSoup(self.page_response.content, "html.parser")
        header_element = soup.find('div', class_='tgme_header_counter')

        if header_element:
            # Вывести кол-во подписчиков
            subscribers_count = header_element.get_text()
            if subscribers_count:
                return {subscribers_count}
            else:
                return "Не удалось определить кол-во подписчиков"

        else:
            return "Не найден хедер"
