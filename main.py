import requests
from bs4 import BeautifulSoup
import re

PAGE = r'https://kz.e-katalog.com/list/122/pr-1356/'


def parsing_site(start_page):
    pages = get_all_pages(get_html(start_page), start_page)
    prices = []
    for page in pages:
        prices += get_price(get_html(page))
    print_info(prices)


def get_html(url):
    response = requests.get(url)
    return response.text


def get_all_pages(html, start_page):
    soup = BeautifulSoup(html, 'html.parser')
    elements = soup.find('div', class_='ib page-num').find_all('a')
    count_pages = 0
    for element in elements:
        try:
            page = int(element.getText())
            if page > count_pages:
                count_pages = page
        except ValueError:
            pass
    pages = [start_page]
    for i in range(1, count_pages):
        pages.append('{}{}/'.format(start_page, i))
    return pages


def get_price(html):
    soup = BeautifulSoup(html, 'html.parser')
    elements = soup.select('div.model-price-range span')
    prices = []
    i = 0
    print('--------------------------------')
    while i < len(elements):
        price_1 = re.sub('\W+', '', elements[i].getText())
        print('price_1', price_1)
        i += 1
        if str(price_1).find('тг') != -1:
            price_1 = str(price_1).replace('тг', '')
            prices.append(int(price_1))
        else:
            price_2 = re.sub('\W+', '', elements[i].getText())
            print('price_2', price_2)
            prices.append((float(price_1) + float(price_2)) / 2)
            i += 1
    return prices


def print_info(prices):
    sum_price = 0
    for price in prices:
        sum_price += price
    print("Среднея цена:", round(sum_price / len(prices), 2))


if __name__ == '__main__':
    parsing_site(PAGE)
