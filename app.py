import requests
from bs4 import BeautifulSoup
import csv

word_search = input('Введите слово для поиска по нему: ')

# URL сайта, который вы хотите парсить
url = 'https://ria.ru/world/'

# Отправляем GET-запрос к сайту
response = requests.get(url)

# Создаем CSV-файл для записи данных
with open('info.csv', 'w', newline='', encoding='utf-8') as csvfile:
    # Определяем заголовки для столбцов в CSV-файле
    fieldnames = ['Дата и время публикации', 'Название статьи', 'Ссылка', 'Текст статьи']

    # Создаем объект записи CSV
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Записываем заголовки в файл
    writer.writeheader()

    # Проверяем, что запрос был успешным
    if response.status_code == 200:
        # Инициализируем объект BeautifulSoup для парсинга страницы
        soup = BeautifulSoup(response.text, 'html.parser')

        # Ищем все элементы с классом 'list-item__title' (название статьи)
        titles = soup.find_all(class_='list-item__title')

        # Ищем все элементы с классом 'list-item__date' (дата и время публикации)
        dates = soup.find_all(class_='list-item__date')

        # Записываем данные в CSV-файл, если в названии статьи есть слово, и получаем текст статьи
        for title, date in zip(titles, dates):
            article_title = title.text.strip()
            article_link = title['href']
            publication_time = date.text.strip()

            # Проверяем, содержит ли название статьи слово
            if word_search in article_title:
                # Отправляем GET-запрос к странице статьи
                article_response = requests.get(article_link)
                if article_response.status_code == 200:
                    # Инициализируем объект BeautifulSoup для парсинга статьи
                    article_soup = BeautifulSoup(article_response.text, 'html.parser')

                    # Ищем текст статьи
                    article_text = article_soup.find_all(class_='article__text')
                    full_text = '\n'.join([item.text.strip() for item in article_text])

                    # Записываем данные в CSV-файл
                    writer.writerow({'Дата и время публикации': publication_time,
                                     'Название статьи': article_title,
                                     'Ссылка': article_link,
                                     'Текст статьи': full_text})

    else:
        print("Ошибка при запросе к сайту. Код состояния:", response.status_code)





#url = 'https://ria.ru/world/'






