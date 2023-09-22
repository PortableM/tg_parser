import json
import schedule
import time
from Parser import Parser, HttpClient, TelegramChannelParser
import asyncio


CHANNELS_LIMIT = 200


def get_channels_from_json(file_name: str, limit: int = 0) -> list:
    """Возвращает список каналов из json"""
    with open(file_name) as file:
        data = json.load(file)
        if limit == 0:
            return [channel_data['alias'][1:] for channel_data in data]
        return [channel_data['alias'][1:] for channel_data in data[:limit]]


async def scrape_telegram_channels(channels):
    results = []
    parser_tasks = []

    http_client = HttpClient(base_url="https://t.me/")

    async def fetch_data(channel: str) -> tuple:
        """Собирает данные о подписчика с канала асинхронно."""
        try:
            telegram_parser = TelegramChannelParser(channel, http_client)
            subscribers_count = await telegram_parser.fetch_subscribers_count()
            results.append((channel, subscribers_count))

        except Exception as e:
            results.append((channel, None))
            print(f"Error scraping data from channel {channel}: {str(e)}")

    for channel in channels:
        task = asyncio.create_task(fetch_data(channel))
        parser_tasks.append(task)

    await asyncio.gather(*parser_tasks)

    return results


def output_text(text, output_file):
    """Записывает текст в отдельный файл"""
    with open(output_file, "w") as file:
        current_time = time.ctime(time.time())
        file.write("Время записи: " + current_time)
        file.write(text)


def multiple_channel_parsing_test():
    """Получаем каналы, парсим, собирает стату и сохранят в файл"""
    # Извлечение данных о каналов
    channels = get_channels_from_json('channels.json', limit=CHANNELS_LIMIT)

    # Парсинг
    print('Начинаем парсить...')
    start = time.time()
    subscribers_count = asyncio.run(
        scrape_telegram_channels(channels))
    print(f"Количество спарсенных каналов: {len(subscribers_count)}")
    end = time.time()
    print(f'Спарсено за {end - start} с.')

    # Статистика
    successfully_parsed = list(
        data[0] + ' ' + data[1] for data in subscribers_count
        if data[1] is not None)
    print(f'Успешно спарсировано: {len(successfully_parsed)}')

    badly_parsed = list(
        data[0] for data in subscribers_count
        if data[1] is None)
    print(f'Неудачно спарсировано: {len(badly_parsed)}')

    # Сохранение в файле
    output_text('\n'.join(successfully_parsed), 'subscribers.txt')
    output_text('\n'.join(badly_parsed), 'bad.txt')


async def test_telegram_channel_parser(channel_name):
    http_client = HttpClient(base_url="https://t.me/")
    parser = TelegramChannelParser(channel_name, http_client)
    subscribers_count = await parser.fetch_subscribers_count()
    print(f"Subscribers count for {channel_name}: {subscribers_count}")
    http_client.close_session()


if __name__ == '__main__':
    # multiple test
    multiple_channel_parsing_test()
    # class_test()

    # default async test
    # channel_name = "python_tricks"
    # asyncio.run(test_telegram_channel_parser(channel_name))


    # # Устанавливаем задачи в schedular.
    # schedule.every().hour.do(multiple_channel_parsing_test)

    # # Поиск задач для выполнения в schedular каждую секунду.
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)
