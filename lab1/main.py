from bs4 import BeautifulSoup
import requests
import re

response = requests.get('https://kpfu.ru/institutes')
soup = BeautifulSoup(response.text, features='html.parser')

founded_institutes = list()
# patterns = ['Структура', 'О нас', 'Институт физики', 'Об институте']
patterns = ['Институт физики']

for institute in soup.find_all('a', text=re.compile('(.+)?[Ии]нститут (.+)?')):
    if institute.text in founded_institutes:
        continue
    founded_institutes.append(institute.text)
    print(institute.text)
    response = requests.get(institute['href'])
    soup = BeautifulSoup(response.text, features='html.parser')
    response = None
    for pattern in patterns:
        if soup.find('a', text=pattern):
            response = requests.get(soup.find('a', text=pattern)['href'])
            break
    if not response:
        continue
    soup = BeautifulSoup(response.text, 'html.parser')
    if soup.find_all('a', text=re.compile('(.+)?Кафед[рp]а(.+)?')):
        print(soup.find_all('a', text=re.compile('(.+)?Кафед[рp]а(.+)?')))
        continue
    if soup.find('a', text='Кафедры'):
        response = requests.get(soup.find('a', text='Кафедры')['href'])
        soup = BeautifulSoup(response.text, 'html.parser')
        if soup.find_all('a', text=re.compile('(.+)?Кафед[рp]а(.+)?')):
            print(soup.find_all('a', text=re.compile('(.+)?Кафед[рp]а(.+)?')))
            continue

