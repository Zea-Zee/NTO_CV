print('works')
import requests
from bs4 import BeautifulSoup

def fetch_data_from_url(url):
    try:
        # Отправляем GET-запрос по указанному URL
        response = requests.get(url)
        response.raise_for_status()  # Проверяем наличие ошибок при запросе
        html = response.text  # Получаем HTML-код страницы

        # Используем BeautifulSoup для парсинга HTML
        soup = BeautifulSoup(html, 'html.parser')

        # Извлекаем описание и ссылку на изображение
        description = soup.find('meta', attrs={'name': 'description'})['content']
        image_url = soup.find('meta', property='og:image')['content']

        return {'description': description, 'image_url': image_url}

    except Exception as e:
        print('Произошла ошибка:', e)
        return None

# Пример вызова функции с URL https://opentripmap.com/ru/card/R2906502
example_url = 'https://opentripmap.com/ru/card/R2906502'
data = fetch_data_from_url(example_url)
if data:
    print('Описание:', data['description'])
    print('URL изображения:', data['image_url'])
else:
    print('Не удалось получить данные.')
