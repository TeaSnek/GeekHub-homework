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
from time import sleep
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


def refresh_file(category):  # create or cleaning file for category
    with open(Path(BASE_DIR, f'category_{category}.json'), 'w') as f:
        f.write('')


if __name__ == '__main__':
    category = get_category()
    startindex = 0
    endindex = 50
    refresh_file(category)
    while True:

        response = requests.get(SEARCH_API, params={
            'searchType': 'category',
            'store': 'Sears',
            'storeId': 10153,
            'catGroupId': category,
            'filterValueLimit': 500,
            'startIndex': startindex,
            'endIndex': endindex,
        }, headers={
            'authority': 'www.sears.com',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'authorization': 'SEARS',
            'cache-control': 'no-cache',
            'content-type': 'application/json',
            'pragma': 'no-cache',
            'sec-ch-ua': '"Opera GX";v="105", "Chromium";v="119"' +
            ', "Not?A_Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
        })

        try:
            data = response.json()
        except requests.exceptions.JSONDecodeError:
            print(response.status_code)
            sleep(60)
            continue

        if 'errors' in data.keys():
            print('Parsed')
            break

        if startindex == 0:
            with open(Path(BASE_DIR, f'category_{category}.json'), 'w') as f:
                for item in data['items']:
                    f.write(json.dumps(item) + '\n')
                print(f'From: {startindex} to {endindex}')

        else:
            with open(Path(BASE_DIR, f'category_{category}.json'), 'a') as f:
                for item in data['items']:
                    f.write(json.dumps(item) + '\n')
                print(f'From: {startindex} to {endindex}')

        sleep(10)
        startindex, endindex = endindex + 1, endindex + 50
