import re
from bs4 import BeautifulSoup
import aiohttp
import asyncio


class Parser:
    def __init__(self, http_client, url):
        self.http_client = http_client
        self.url = url

    async def fetch_content(self):
        content = await self.http_client.get(self.url)
        return content


class TelegramChannelParser:
    def __init__(self, channel_name: str, http_client):
        self.channel_name = channel_name
        self.http_client = http_client

    async def fetch_subscribers_count(self):
        """
        Получает данные о кол-ве субскриберов на канал\
        Использует название канала как относительный url
        """
        url = self.channel_name
        # Получаем контент страницы
        self.parser = Parser(self.http_client, url)
        channel_content = await self.parser.fetch_content()

        # Определяем кол-во подписчиков
        soup = BeautifulSoup(channel_content, "html.parser")
        target_element = soup.find('div', class_='tgme_page_extra')

        if target_element:
            # Вывести кол-во подписчиков
            subscribers_count = target_element.get_text()
            if subscribers_count:
                subscribers_count = re.sub(r'\D', '', subscribers_count)
                return subscribers_count

            return None

        return None


class HttpClient:
    def __init__(self, base_url=None):
        self.base_url = base_url
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
            AppleWebKit/537.36 (KHTML, like Gecko)\
            Chrome/96.0.4664.110 Safari/537.36"
        }
        self.session = aiohttp.ClientSession(
            base_url=self.base_url,
            headers=self.headers
        )

    async def get(self, url):
        try:
            # Объединяем url, если есть базовый url.
            if self.base_url:
                url = '/' + url

            # Получаем контент страницы
            async with self.session.get(url) as response:
                response.raise_for_status()
                content = await response.content.read()
                return content

        except aiohttp.ClientError as e:
            print(f"HTTP request error occurred: {str(e)}")
            return None

        except asyncio.TimeoutError as e:
            print(f'HTTP request timed out: {str(e)}')
            return None

    async def close_session(self):
        await self.session.close()
