'''
Створіть програму для отримання курсу валют за певний період.
- отримати від користувача дату (це може бути як один день так і інтервал -
    початкова і кінцева дати, продумайте механізм реалізації) і назву валюти
- вивести курс по відношенню до гривні на момент вказаної дати (або за кожен
    день у вказаному інтервалі)
- не забудьте перевірку на валідність введених даних
'''

import requests
import datetime as dt
import re

AVALIABLE_CODES = [
    'USD',
    'EUR',
    'CHF',
    'GBP',
    'PLZ',
    'SEK',
    'XAU',
    'CAD',
]


def validate_date(text: str) -> None:
    if re.fullmatch(r'\d{1,2}[\.]\d{1,2}[\.](?!0000)\d{4}', text):
        user_date = dt.datetime.strptime(text, '%d.%m.%Y')
        if user_date > dt.datetime.today():
            raise ValueError('Date cannont be from future')
        elif (dt.datetime.today() - user_date).days / 365.24 > 4:
            raise ValueError('Cant get more than 4 years')
    else:
        raise ValueError(f'Unsupported template "{text}"')


if __name__ == '__main__':
    target_currency = ''
    start_day = ''
    end_day = ''
    today_text = dt.datetime.today().strftime('%d.%m.%Y')

    while target_currency not in AVALIABLE_CODES:
        target_currency = input('Input correct currency code: ').upper()

    while (not (start_day and end_day)) or (start_day > end_day):
        buffer = start_day if start_day else today_text
        buffer = input(f'From date: {buffer}\033[{len(buffer)}D')
        start_day = buffer if buffer else today_text
        try:
            validate_date(start_day)
        except ValueError as e:
            print(e)
            start_day = ''
            continue

        buffer = end_day if end_day else today_text
        buffer = input(f'To date: {buffer}\033[{len(buffer)}D')
        end_day = buffer if buffer else today_text
        try:
            validate_date(end_day)
        except ValueError:
            end_day = ''
            continue

    start = dt.datetime.strptime(start_day, '%d.%m.%Y')
    end = dt.datetime.strptime(end_day, '%d.%m.%Y')
    list_of_dates = [start + dt.timedelta(days=delta)
                     for delta in range((end - start).days + 1)]

    for date in list_of_dates:
        api_url = 'https://api.privatbank.ua/p24api/exchange_rates'
        request = requests.get(
            url=api_url,
            params={
                'date': date.strftime('%d.%m.%Y')
            }
        )
        data = request.json()['exchangeRate']
        try:
            target_data = [exch for exch in data
                           if exch['currency'] == target_currency][0]
        except IndexError:
            target_data = {
                'saleRate': float('nan'),
                'purchaseRate': float('nan')
            }
        print('UAH/{} || SALE: {:.2f} || PURCHASE: {:.2f} || DATE: {}'.format(
            target_currency,
            target_data['saleRate'],
            target_data['purchaseRate'],
            date.strftime('%d.%m.%Y')
            )
        )
