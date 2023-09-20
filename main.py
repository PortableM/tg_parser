import json
import schedule
import time
from Parser import Parser
from multiprocessing import Pool, cpu_count

PARSE_AMOUNT = 1000


def init_parsers(file_name):
    """Возвращает список парсеров для каждого канала"""
    parsers = []

    with open(file_name) as file:
        data = json.load(file)
        for channel_data in data:
            channel_name = channel_data['alias'][1:]
            parsers.append(Parser(channel_name, default_page=False))
            if len(parsers) >= PARSE_AMOUNT:
                break

    return parsers


def output_text(text, output_file):
    """Записывает текст в отдельный файл"""
    with open(output_file, "a") as file:
        current_time = time.ctime(time.time())
        file.write("Время записи: " + current_time)
        file.write(text)


def parse_channel(channel_parser):
    """Парсит канал и возвращает количество подписчиков"""
    channel_parser.parse()
    count = channel_parser.get_subscribers_count()

    return f"{channel_parser.get_name()}: {count}"


def parse_subscribers_count():
    parsers = init_parsers('channels.json')
    print('Начинаем парсировать...')

    # Запускаем несколько процессов
    num_cores = cpu_count()
    print(f"Использовано ядер: {num_cores}")
    pool = Pool(processes=num_cores)

    # Запускаем parse_channel параллельно
    results = pool.map(parse_channel, parsers)
    subscribers_count = '\n'.join(results)

    # Принт резузльтатов в файл
    output_text(subscribers_count, 'subscribers.txt')


def performance_test():
    """Замер скорости работы"""
    print("Запуск бота...")
    start_time = time.time()
    parse_subscribers_count()
    end_time = time.time()
    print("Данные собраны!")
    print(f"Спарсили {PARSE_AMOUNT} каналов за {end_time - start_time} секунды")


if __name__ == '__main__':
    performance_test()

    # Устанавливаем задачи в schedular.
    schedule.every().hour.do(parse_subscribers_count)

    # Поиск задач для выполнения в schedular каждую секунду.
    while True:
        schedule.run_pending()
        time.sleep(1)
