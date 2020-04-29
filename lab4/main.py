from bs4 import BeautifulSoup
import requests
import urllib.request as req
from urllib.parse import quote
import re


def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    rq = requests.get(url, headers=headers)
    return rq.text


keyword = input('Введите название или ключевые слова вакансии на hh.ru: ')
URL = 'https://kazan.hh.ru/search/vacancy?area=88&st=searchVacancy&text={}'.format(quote(keyword))
soup = BeautifulSoup(get_html(URL), 'html.parser')

for _ in soup.find_all('div', {"class": 'vacancy-serp-item'}):
    a = _.find('div', {'class': 'vacancy-serp-item__info'}).find('a')
    print(a.text)
    print('Полное описание: {}'.format(a['href']))
    soup = BeautifulSoup(get_html(a['href']), 'html.parser')
    p = soup.find('div', {'class': 'vacancy-description'}).find('div', {'class': 'bloko-gap bloko-gap_bottom'})
    clean = re.compile('<.*?>')
    p = re.sub(clean, '', str(p))
    print(p.replace('года', 'года. ').replace('лет', 'лет. ').strip())
    salary = soup.find('p', {'class': 'vacancy-salary'})
    salary = re.sub(clean, '', str(salary))
    print(salary)
    print()
