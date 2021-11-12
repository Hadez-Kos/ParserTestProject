from selenium import webdriver
from bs4 import BeautifulSoup
import selenium.webdriver.common.devtools.v93 as devtools

options = webdriver.ChromeOptions()

options.add_experimental_option('prefs', {
    'geolocation': True
})

try:
    driver = webdriver.Chrome(
        executable_path='yandexdriver.exe',
        options=options
    )

    url = 'https://www.detmir.ru/catalog/index/name/zdorovyj_perekus_pp/'

    driver.execute_cdp_cmd('Network.setUserAgentOverride', {
        'userAgent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.85 YaBrowser/21.11.0.1996 Yowser/2.5 Safari/537.36',
        'platform': 'Windows'})

    driver.execute_cdp_cmd("Emulation.setGeolocationOverride", {"latitude": 59.9386,
                                                                "longitude": 30.3141,
                                                                "accuracy": 50})

    page = 1
    while True:
        url_page = url + f"page/{page}/"
        driver.get(url=url_page)

        soup = BeautifulSoup(driver.page_source, 'lxml')
        try:
            html_tag_product = soup.find('div', class_='cc').find('div', class_='cj').find('div', class_='oX')
            city = soup.find('span', class_='yV').text
            for i in html_tag_product.find_all('div', attrs={
                'class': ['wR w_2 oY wW', 'wR w_2 oY wW w_0', 'wR wZ oY wU', 'wR w_2 oY']}):
                url_product = i.find('a', attrs={'class': ['Ni NK', 'Ni NK Nj']}).get('href')
                Id_product = int(url_product.split('/id', 1)[1].replace('/', ''))
                title_product = i.find('p', class_='Nl').text
                print(url_product, Id_product, title_product, city, page)

            page += 1
        except:
            break


except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()
