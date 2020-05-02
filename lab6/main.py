# Спарсить расписание с сайта университета и отправить себе на почту
from bs4 import BeautifulSoup
import requests

URL = 'https://kpfu.ru/subject_schedule_web.schedule_type_study?p_faculty=9&p_speciality=1&p_course=3&p_group=24358&p_poisk=1&p_portal=&p_not_top=&p_sub='
response = requests.get(URL)

soup = BeautifulSoup(response.content, 'html.parser')

weekdays = {
    '0': 'Понедельник',
    '1': 'Вторник',
    '2': 'Среда',
    '3': 'Четверг',
    '4': 'Пятница',
    '5': 'Суббота',
    '6': 'Воскресенье'
}

lessons = [[] for _ in range(6)]

trs = soup.find_all('table')[2].find_all('tr')
for tr in trs:
    tds = tr.find_all('td')
    time = 0
    for i, td in enumerate(tds):
        if i == 0:
            time = td.text
            continue
        spans = td.find_all('span')
        if spans:
            for span in spans:
                lessons[i - 1].append('{}: {}'.format(time, span.text))

result = ''

for day, lesson in enumerate(lessons):
    print(weekdays[str(day)] + ":")
    result += weekdays[str(day)] + ":\n"
    for less in lesson:
        print(less)
        result += less + "\n"
    print()
    result += "\n"

import smtplib
from email.mime.text import MIMEText

msg = MIMEText(result)

msg['Subject'] = "Расписание Прикладной математики 09-721"
msg['From'] = "testlabapython@mail.ru"
msg['To'] = "inuur@mail.ru"

s = smtplib.SMTP_SSL('smtp.mail.ru', 465)
s.login('testlabapython@mail.ru', 'pythonlaba123')
s.send_message(msg)
s.quit()
