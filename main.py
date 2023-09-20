import schedule
import time
from Parser import Parser


def input_channels():
    """Возвращает список парсеров для каждого канала"""
    channels = []
    while channel := input("Введите название канала: "):
        channels.append(Parser(channel, default_page=False))

    return channels


def print_subscribers_count():
    """Выводит кол-во подписчиков для списка каналов."""
    for channel in target_channels:
        channel.parse()
        count = channel.get_subscribers_count()
        print(f"Количество подписчиков канала {channel.get_name()}: {count}")


target_channels = input_channels()

# Принт резузльтатов сразу
print_subscribers_count()

# Устанавливаем задачи в scedular.
# Пока каждые 10 секунд, чтобы сразу видеть работу.
schedule.every().hour.do(print_subscribers_count)

# Поиск задач для выполнения в schedular каждую секунду.
while True:
    schedule.run_pending()
    time.sleep(1)
