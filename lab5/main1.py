# Разработать веб- краулер с глубиной поиска до 6 ссылок, с помощью
# которого скачать все документы в форматах xls, xlsx, pdf c сайта
# института (urllib.urlretrieve либо open/write).
# ТАК КАК ИДЕТ РАНДОМНЫЙ ВЫБОР САЙТА ИЗ СПИСКА ТО КОЛ-ВО НАЙДЕННЫХ ФАЙЛОВ ВСЕГДА РАЗНОЕ
# ИНОГДА МНОГО ИНОГДА МАЛО.
# ПЕРЕД ЗАПУСКОМ ВСЕ ФАЙЛЫ УДАЛЯЮТСЯ
import requests
from bs4 import BeautifulSoup
import random
import os

file_list = [f for f in os.listdir('files')]
for f in file_list:
    os.remove(os.path.join('files', f))

start_ulr = 'https://kpfu.ru/computing-technology'
depth = 6
patterns = ['.pdf', '.xlx', 'xlsx']
all_files = []


def go_depth(url, max_depth, current_depth=1):
    print('Парсим на {} глубине'.format(current_depth))
    global all_files
    files = []
    found_links = []
    proceeded_links = 0

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    a = soup.find_all('a')

    for _ in a:
        try:
            href = str(_['href'])
            if not href.startswith('http'):
                continue
            for pattern in patterns:
                if href.endswith(pattern):
                    files.append(href)
                    break
            if '.' in href.split('/')[-1]:
                continue
            found_links.append(href)
        except KeyError:
            continue
    print('Найдено {} файлов'.format(len(files)))
    print()

    all_files = all_files + files
    if current_depth == max_depth:
        return

    # Берем 3 рандомных сайта и парсим их тем же образом
    random.shuffle(found_links)
    go_depth(found_links[0], max_depth, current_depth=current_depth + 1)


go_depth(start_ulr, depth)
print('Найдено всего {} файлов'.format(len(all_files)))
for file in all_files:
    file_name = file.split('/')[-1]
    with open('files/{}'.format(file_name), 'wb') as f:
        f.write(requests.get(file).content)
    print(file)
