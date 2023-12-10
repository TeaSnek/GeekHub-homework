"""
1. Викорисовуючи requests, написати скрипт, який буде приймати на вхід ID
категорії із сайту https://www.sears.com і буде збирати всі товари із цієї
категорії, збирати по ним всі можливі дані (бренд, категорія, модель, ціна,
рейтинг тощо) і зберігати їх у CSV файл (наприклад, якщо категорія має ID
12345, то файл буде називатись 12345_products.csv)

Наприклад, категорія https://www.sears.com/tools-tool-storage/b-1025184 має ІД
1025184
"""

import requests
import json
from pathlib import Path

SEARCH_API = 'https://www.sears.com/api/sal/v3/products/search'
BASE_DIR = Path(__file__).parent


def get_category():
    while True:
        print('Input category id:')
        try:
            return int(input('Input: '))
        except ValueError:
            print('Invalid category id, it must be a number')


if __name__ == '__main__':
    category = get_category()
    response = requests.get(SEARCH_API, params={
        'searchType': 'category',
        'store': 'Sears',
        'storeId': 10153,
        'catGroupId': category,
        'filterValueLimit': 500,
        'endIndex': 300,
    }, headers={
        'Authorization': 'SEARS'
    })
    data = response.json()
    if 'errors' in data.keys():
        print('Something went wrong')
        exit()

    with open(Path(BASE_DIR, f'category_{category}.json'), 'w') as f:
        for item in data['items']:
            print(json.dumps(item), file=f, end='\n')
