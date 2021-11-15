from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd


def get_info_product(url, city, coord):
    options = webdriver.ChromeOptions()

    options.add_experimental_option('prefs', {'geolocation': True})

    options.headless = True

    try:
        driver = webdriver.Chrome(executable_path='../yandexdriver.exe', options=options)

        driver.execute_cdp_cmd('Network.setUserAgentOverride', {
            'userAgent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.85 YaBrowser/21.11.0.1996 Yowser/2.5 Safari/537.36',
            'platform': 'Windows'})

        driver.execute_cdp_cmd("Emulation.setGeolocationOverride", coord)
        page = 1
        list_data_product = []
        while True:
            url_page = url + f"page/{page}/"
            driver.get(url=url_page)
            soup = BeautifulSoup(driver.page_source, 'lxml')
            try:
                html_tag_product = soup.find('div', class_=['cc', 'cC']).find('div', class_='cj').find('div',
                                                                                                       class_=['oQ',
                                                                                                               'oX'])
                for i in html_tag_product.find_all('div', attrs={
                    'class': ['xV x_6 oR x_', 'xV x_6 oR x_ x_4', 'xV x_5 oR x_', 'xV x_5 oR x_ x_4', 'y_6 zh oY zb zg',
                              'y_6 zh oY zb']}):
                    url_product = i.find('a', attrs={'class': ['NA N_1', 'NA N_0', 'Oj OK']}).get('href')
                    id_product = int(url_product.split('/id', 1)[1].replace('/', ''))
                    info_product = i.find('p', attrs={'class': ['ND', 'Om']}).text
                    price = i.find('p', attrs={'class': ['ND', 'Ox']}).text.strip().replace(',', '.').split()[0]
                    try:
                        promo_price = i.find('p', attrs={'class': ['Oy']}).text.replace(',', '.').split()[0]
                    except:
                        promo_price = 'Отсутствует'

                    if promo_price != 'Отсутствует':
                        promo_price, price = price, promo_price

                    list_data_product.append([
                        id_product,
                        info_product,
                        price,
                        city,
                        promo_price,
                        url_product

                    ])

                page += 1
            except:
                break


    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()

    return list_data_product


def write_data_csv(data_parse, columns):
    data = pd.DataFrame(data_parse, columns=columns)
    data.to_csv('parse_date.csv', encoding='utf-8', index=False)


if __name__ == "__main__":
    url_address = 'https://www.detmir.ru/catalog/index/name/zdorovyj_perekus_pp/'
    coord_city = {'Москва': {"latitude": 59.9386, "longitude": 30.3141, "accuracy": 50},
                  'Санкт-Петербург': {"latitude": 55.7522, "longitude": 37.6156, "accuracy": 50}}
    column = ['ID товара', 'Наименование', 'Цена', 'Город', 'Промо цена', 'Ссылка на страницу']
    data_parse_site = []
    for city in coord_city.keys():
        data_parse_site += get_info_product(url=url_address, city=city, coord=coord_city[city])

    write_data_csv(data_parse_site, column)
