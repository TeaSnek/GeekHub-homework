"""
Викорисовуючи requests, заходите на ось цей сайт
"https://www.expireddomains.net/deleted-domains/" (з ним будьте обережні),
вибираєте будь-яку на ваш вибір доменну зону і парсите список  доменів - їх
там буде десятки тисяч (звичайно ураховуючи пагінацію). Всі отримані значення
зберігти в CSV файл.
"""

from pathlib import Path
from random import randint
from time import sleep

import bs4
import requests

base_domain = 'https://www.expireddomains.net'

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

BASE_DIR = Path(__file__).parent


def set_csv_headers():
    with open(Path(BASE_DIR, 'domains.csv'), 'w') as f:
        f.write('domain,backlinks,domainpop,birth,' +
                'archive_crawls,dotcom_status,dotnet_status,' +
                'dotorg_status,tlds_regs,related_domains,' +
                'dropped,status\n')


def parse_table(table_selector: bs4.ResultSet):
    parsed_table = []
    for row in table_selector:
        if not row.select_one('td.field_domain'):
            continue
        row_dict = {
            'domain': row.select_one('td.field_domain a'),
            'backlinks': row.select_one('td.field_bl a'),
            'domainpop': row.select_one('td.field_domainpop a'),
            'birth': row.select_one('td.field_abirth a'),
            'archive_crawls': row.select_one('td.field_aentries a'),
            'dotcom_status': row.select_one('td.field_statuscom a'),
            'dotnet_status': row.select_one('td.field_statusnet a'),
            'dotorg_status': row.select_one('td.field_statusorg a'),
            'tlds_regs': row.select_one('td.field_statustld_registered'),
            'related_domains': row.select_one('td.field_related_cnobi'),
            'dropped': row.select_one('td.field_changes'),
            'status': row.select_one('td.field_whois a'),
            }

        row_texted_dict = {}
        for key, selector in row_dict.items():
            if selector:
                try:
                    row_texted_dict[key] = int(selector.text)
                except ValueError:
                    row_texted_dict[key] = selector.text
            else:
                row_texted_dict[key] = ''
        parsed_table.append(row_texted_dict)
    return parsed_table


if __name__ == '__main__':
    set_csv_headers()
    next_page = base_domain + '/deleted-domains/'
    while next_page:
        headers = {
            'authority': 'www.expireddomains.net',
            'accept': 'text/html,application/xhtml+xml,application/xml;' +
            'q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,' +
            'application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'sec-ch-ua': '"Chromium";v="118", "Opera GX";v="104", ' +
            '"Not=A?Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': USER_AGENTS[randint(0, 9)]
        }
        response = requests.get(next_page, headers=headers)
        soup = bs4.BeautifulSoup(response.text, 'html.parser')
        table_rows = soup.select('table.base1 tr')

        if not table_rows:
            print('Thats all')
            break

        parsed_table = parse_table(table_rows)
        try:
            with open(Path(BASE_DIR, 'domains.csv'), 'a') as f:
                for domain in parsed_table:
                    f.write(','.join([str(value) for value in domain.values()])
                            + '\n')
        except FileNotFoundError:
            with open(Path(BASE_DIR, 'domains.csv'), 'w') as f:
                for domain in parsed_table:
                    f.write(','.join([str(value) for value in domain.values()])
                            + '\n')

        next_page_selector = soup.select_one('a.next')
        if next_page_selector:
            next_page = base_domain + str(next_page_selector.get('href'))
        print(next_page)
        sleep(5)
