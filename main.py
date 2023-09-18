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

    # Найти последний пост
    post_elements = soup.select(".tgme_widget_message")
    last_post_element = post_elements[-1] if post_elements else None

    if last_post_element:
        # Найти кол-во лайков последнего поста
        view_count_element = last_post_element.select_one('.tgme_widget_message_views')
        view_count = view_count_element.get_text()
        if view_count:
            print(f"Количество просмотров последнего поста: {view_count}")
        else:
            print("Нет количества просмотров")

    else:
        print("Не найдено постов")

except requests.exceptions.RequestException as e:
    print(f"Ошибка: {e}")
