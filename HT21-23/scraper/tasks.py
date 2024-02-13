"""
1. Викорисовуючи requests, написати скрипт, який буде приймати на вхід ID
категорії із сайту https://www.sears.com і буде збирати всі товари із цієї
категорії, збирати по ним всі можливі дані (бренд, категорія, модель, ціна,
рейтинг тощо) і зберігати їх у CSV файл (наприклад, якщо категорія має ID
12345, то файл буде називатись 12345_products.csv)

Наприклад, категорія https://www.sears.com/tools-tool-storage/b-1025184 має ІД
1025184
"""
from __future__ import absolute_import, unicode_literals

from random import randint
from time import sleep

from celery import shared_task
import requests

from products.models import (
    Category,
    Product,
)
SEARCH_API = 'https://www.sears.com/api/sal/v3/products/search'
SEARCH_PROD_API = 'https://www.sears.com/api/sal/v3/products/details/'
SITE_BASE = 'https://www.sears.com'

USER_AGENTS = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15) AppleWebKit/605.1.15 ' +
    '(KHTML, like Gecko) Version/13.0.5 Safari/605.1.15',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) ' +
    'Chrome/103.0.5060.53 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Windows; x64) AppleWebKit/537.36 (KHTML, ' +
    'like Gecko) Chrome/103.0.5060.114 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/603.3.8 ' +
    '(KHTML, like Gecko) Version/10.1.2 Safari/603.3.8',
    'Mozilla/5.0 (Windows NT 10.0; Windows; x64) AppleWebKit/537.36 (KHTML, ' +
    'like Gecko) Chrome/103.0.5060.114 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 ' +
    '(KHTML, like Gecko) Version/14.0 Safari/605.1.15',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) ' +
    'Chrome/103.0.5060.53 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 ' +
    '(KHTML, like Gecko) Version/14.0 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Windows; x64) AppleWebKit/537.36 (KHTML, ' +
    'like Gecko) Chrome/103.0.5060.114 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) ' +
    'Chrome/103.0.5060.53 Safari/537.36'
]

headers = {
    'authority': 'www.sears.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'authorization': 'SEARS',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'pragma': 'no-cache',
}


def generate_headers():
    random_headers = headers.copy()
    random_headers['user-agent'] = USER_AGENTS[randint(0, len(USER_AGENTS)-1)]
    return random_headers


def excract_category(categories):
    result = [Category.objects.get(pk='All')]
    for category in categories:
        result.append(
            Category.objects.get_or_create(name=category['name'])[0])
    return result


@shared_task
def save_product_v2(product_data):
    """
    Creates or updates record in db
    """
    prod_details = product_data['productDetail']['softhardProductdetails'][0]
    categories = excract_category(
        prod_details['hierarchies']['specificHierarchy'])
    defaults = {
        'product_name': prod_details['descriptionName'].lower(),
        'price': prod_details['salePrice'],
        'sears_id': prod_details['identity']['sSin'],
        'brand': prod_details['brandName'],
        'sears_link': SITE_BASE + prod_details['seoUrl'],
        'short_about': prod_details['shortDescription']
        if prod_details['shortDescription'] else ''
    }

    obj, created = Product.objects.update_or_create(
        sears_id=prod_details['identity']['sSin'],
        defaults=defaults,
    )
    if created:
        obj.save()
    obj.category.add(*categories)
    return created


@shared_task
def scrape_prod(products_list):
    i = 0

    while i < len(products_list):
        product = products_list[i].upper()
        response = requests.get(SEARCH_PROD_API + product, params={
            'storeName': 'Sears'
        }, headers=generate_headers())

        if response.status_code == 200:
            data = response.json()
            save_product_v2.delay(data)
            i += 1

        elif response.status_code == 404:
            print(f'Product {product} not found')
            i += 1

        elif response.status_code == 429:
            print('Request limited, waiting...')
            sleep(60)
