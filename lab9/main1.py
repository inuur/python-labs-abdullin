# http://pythonscraping.com/comment/reply/10
# 3 Разработать программу (бота) для чтения CAPTCHA (Completely
# Automated Public Turing test to tell Computers and Humans Apart).
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# РАБОТАЕТ ТОЛЬКО ДЛЯ CHROME ВЕРСИИ 81.**
# Для других версий нужно скачать другой ChromeDriver в папку lab10
driver = webdriver.Chrome(executable_path='chromedriver.exe')

driver.get('https://formspree.io/register')
# Вводим почту
driver.find_element_by_name('email').send_keys('test@mail.ru')
# Вводим пароль
driver.find_element_by_name('password').send_keys('testpassword')
# Ставим галку в чекбокс
driver.find_element_by_name('agree').click()
# Отправляем запрос.
driver.find_element_by_xpath('//*[@id="register-form"]/button').click()


