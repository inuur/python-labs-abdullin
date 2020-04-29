from bs4 import BeautifulSoup as BSoup
from urllib.parse import quote
import requests
import re

to_find = input('Введите тематику книг: ')
to_find = to_find.replace(' ', '+')
URL = 'https://allfind.kpfu.ru/Search/Results?lookfor={}&type=AllFields'.format(quote(to_find))

response = requests.get(URL)
soup = BSoup(response.text, 'html.parser')
books = soup.find_all('div', {'class': 'result clearfix'})
for book in books:
    block = book.find('div', {'class': 'record-title'}).find('a')
    response = requests.get('https://allfind.kpfu.ru' + block['href'] + '/Holdings#tabnav')
    soup = BSoup(response.text, 'html.parser')
    title = soup.find('h3').text
    print('Название: ', title)
    authors = soup.find('tr').find('td').text
    print('Авторы: ', authors.strip())
    print('Описание:')
    tables = soup.find_all('table')
    description = tables[-1].find('tr')
    if description.find('th').text.strip() == 'Аннотация:':
        print(description.find('td').text.strip())
    else:
        print('Отсутствует')
    link = tables[0]
    link = link.find('th', text='Онлайн ссылка: ')
    if link:
        print('Тип: Электронный')
        print('Режим доступа: ', link.parent.find('td').text.strip())
    else:
        print('Тип: Бумажный')
        status = soup.find_all('span', {'class': re.compile('text-(success|danger)')})
        for status in status:
            if 'доступно' in status.text.lower():
                print('Доступно')
                break
        else:
            print('Не доступно')
    print()
if not books:
    print('По данному запросу ничего не найденно!')
