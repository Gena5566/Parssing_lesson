import requests
from bs4 import BeautifulSoup

# Функция для получения всех ссылок на странице
def get_links(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a')
        return [link.get('href') for link in links if link.get('href')]
    else:
        print("Ошибка при получении страницы:", response.status_code)
        return []

# Функция для получения списка моделей с указанной страницы
def get_car_models(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        models_info = soup.find('ul', {'class': 'model-list'})
        if models_info:
            model_links = models_info.find_all('a')
            model_names = [link.text.strip() for link in model_links]
            return model_names
        else:
            print("Информация о моделях не найдена на странице.")
            return []
    else:
        print("Ошибка при получении страницы:", response.status_code)
        return []

# Функция для вывода HTML-кода страницы
def print_html(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        print(soup.prettify())
    else:
        print("Ошибка при получении страницы:", response.status_code)

# Функция для получения списка моделей из раздела "Модельный ряд"
def get_models_from_section(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        section_title = soup.find('a', class_='u115-00__section-title', text='Модельный ряд')
        if section_title:
            section = section_title.find_parent('div')
            model_items = section.find_all('li')
            models = [item.find('a').text.strip() for item in model_items]
            return models
        else:
            print("Информация о моделях не найдена на странице.")
            return []
    else:
        print("Ошибка при получении страницы:", response.status_code)
        return []

if __name__ == "__main__":
    main_url = "https://kaiyi-auto.ru/"
    models_url = "https://kaiyi-auto.ru/models/"

    # Получение всех ссылок на главной странице
    print("Ссылки на главной странице:")
    main_links = get_links(main_url)
    for link in main_links:
        print(link)

    # Получение списка моделей с страницы моделей
    print("\nСписок моделей автомобилей:")
    car_models = get_car_models(models_url)
    for model in car_models:
        print(model)

    # Вывод HTML-кода страницы моделей
    print("\nHTML-код страницы моделей:")
    print_html(models_url)

    # Получение списка моделей из раздела "Модельный ряд"
    print("\nМодели из раздела 'Модельный ряд':")
    models_from_section = get_models_from_section(models_url)
    for model in models_from_section:
        print(model)








