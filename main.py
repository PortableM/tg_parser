import json
import schedule
import time
from Parser import Parser
from multiprocessing import Pool, cpu_count


PARSE_AMOUNT = 10


def get_channels_from_json(file_name: str, limit: int = 0) -> list:
    """Возвращает список каналов из json"""
    with open(file_name) as file:
        data = json.load(file)
        if limit == 0:
            return [channel_data['alias'][1:] for channel_data in data]
        return [channel_data['alias'][1:] for channel_data in data[:limit + 1]]


def init_parsers(channels: list) -> list:
    """Возвращает список парсеров для каждого канала"""
    return [Parser(channel_name, default_page=False)
            for channel_name in channels]


def parse_channel(channel_parser):
    """Парсит канал и возвращает количество подписчиков"""
    channel_parser.parse()
    count = channel_parser.get_subscribers_count()

    return f"{channel_parser.get_name()}: {count}"


def output_text(text, output_file):
    """Записывает текст в отдельный файл"""
    with open(output_file, "a") as file:
        current_time = time.ctime(time.time())
        file.write("Время записи: " + current_time)
        file.write(text)


def performance_test():
    channels_names = get_channels_from_json('channels.json',
                                            limit=PARSE_AMOUNT)
    parsers = init_parsers(channels_names)

    # Включаем мультипроцессинг
    num_cores = cpu_count()
    print(f"Использовано ядер: {num_cores}")
    pool = Pool(processes=num_cores)

    # Количество субскриберов для каждого канала
    subscribers_count_list = pool.map(parse_channel, parsers)

    # Принт результатов
    output_text('\n'.join(subscribers_count_list), 'subscribers.txt')


if __name__ == '__main__':
    performance_test()

    # Устанавливаем задачи в schedular.
    schedule.every().hour.do(performance_test)

    # Поиск задач для выполнения в schedular каждую секунду.
    while True:
        schedule.run_pending()
        time.sleep(1)
