from selenium import webdriver
from bs4 import BeautifulSoup
import time

options = webdriver.ChromeOptions()
category_product = {}
try:
    driver = webdriver.Chrome(
        executable_path='yandexdriver.exe',
        options=options
    )

    driver.get(url='https://www.detmir.ru')
    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, 'lxml')
    for category in soup.find('div', class_='kX').find('ul', class_='kL').find_all('li', attrs={'class': 'kM'}):
        tag_a = category.find('a', class_='kN')
        if not (tag_a is None) and 'catalog' in tag_a.get('href'):
            category_product[tag_a.text] = tag_a.get('href')
    print(category_product)
except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()

