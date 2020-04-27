from bs4 import BeautifulSoup
import requests
import re

response = requests.get('https://kpfu.ru/physics')
soup = BeautifulSoup(response.text, features='html.parser')
founded_cafedras = list()
# print(soup.prettify())
for _ in soup.find_all('a', text='Институт физики'):
    print(_)
