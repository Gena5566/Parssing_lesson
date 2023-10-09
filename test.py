from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

# Инициализируем веб-драйвер
driver = webdriver.Chrome()

# Создаем список для хранения информации о элементах
elements_info = []

# Начальный номер страницы
page_number = 0

while True:
    # Формируем URL-адрес с номером страницы
    url = f'https://market.yandex.ru/catalog--smartfony/26893750/list?rs=eJwdUCurQkEY3KNJ_AWCwpoNos0XHE3CRRAxXuEk8T9YDj7AICabZbMoaLD4wHODiE0QwwXBgyI2g3AV292ZMgwz3zfz7cYb3qKxMYSoZjRa5ZRG55bWaF4WGu1jUqPbg-I84YoRdNMm_4EuOkAVXGK-wK07FHcCbs3pRuCqPpUjuPwCihJ6zTBzWnDllvMzoP2dQM6H90yB1h963foafAdXxrhbYeMQmWaemW_qPnDZBKo0bzDoRtGlunxvm10v9h740jHdAXv3_IER-S8nT9iyrrxHUg-toOfY6GG-n5OKaQEmn_k_Nmey4M6DLbXUP1YoiHA%2C&hid=91491&allowCollapsing=1&local-offers-first={page_number}'

    # Открываем страницу
    driver.get(url)

    # Ожидаем, пока загрузятся элементы
    wait = WebDriverWait(driver, 10)
    elements = wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[data-index]')))

    # Получаем информацию о элементах
    for element in elements:
        text = element.text
        href_value = element.get_attribute('href')
        elements_info.append({'text': text, 'href': href_value})

    # Прокручиваем страницу вниз с использованием JavaScript
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Добавляем задержку между прокрутками
    time.sleep(1)

    # Проверяем, есть ли следующая страница
    next_button = driver.find_elements(By.CSS_SELECTOR, 'a[aria-label="Следующая страница"]')
    if not next_button:
        break

    # Увеличиваем номер страницы перед следующей итерацией
    page_number += 1

# Выводим информацию о каждом элементе
for index, element_info in enumerate(elements_info, start=1):
    print(f"Элемент {index}:")
    print("Текст элемента:", element_info['text'])
    print("Значение атрибута 'href':", element_info['href'])
    print("\n")

# Закрываем браузер
driver.quit()

# Записываем данные в CSV файл
csv_filename = 'elements_info.csv'
with open(csv_filename, mode='w', newline='', encoding='utf-8') as csv_file:
    fieldnames = ['text', 'href', 'tag_name']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()
    for element_info in elements_info:
        writer.writerow(element_info)

print(f"Данные записаны в {csv_filename}")







