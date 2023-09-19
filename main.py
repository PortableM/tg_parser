import requests
from bs4 import BeautifulSoup

channel_name = input("Введите название канала: ")
target_url = f"https://t.me/s/{channel_name}"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
}

try:
    page_response = requests.get(target_url, headers=headers)
    page_response.raise_for_status()
    soup = BeautifulSoup(page_response.content, "html.parser")

    # Определяем кол-во подписчиков
    header_element = soup.find('div', class_='tgme_header_counter')

    if header_element:
        # Вывести кол-во подписчиков
        subscribers_count = header_element.get_text()
        if subscribers_count:
            print(f"Количество подписчиков канала: {subscribers_count}")
        else:
            print("Не удалось определить кол-во подписчиков")

    else:
        print("Не найден хедер")

except requests.exceptions.RequestException as e:
    print(f"Ошибка: {e}")
