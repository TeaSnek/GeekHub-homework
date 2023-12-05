"""
http://quotes.toscrape.com/ - написати скрейпер для збору всієї доступної
інформації про записи: цитата, автор, інфа про автора тощо.
- збирається інформація з 10 сторінок сайту.
- зберігати зібрані дані у CSV файл
"""

import requests
import bs4
from pathlib import Path

BASE_PAGE = 'http://quotes.toscrape.com'
BASE_DIR = Path(__file__).parent


def process_author(url: str):
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    author_born = 'Unknown'
    author_about = 'Unknown'
    author_born_info = soup.select_one('span.author-born-date')
    author_about_info = soup.select_one('div.author-description')
    if author_born_info is not None:
        author_born = author_born_info.text

    filter_chars = ['\n', '\t']
    if author_about_info is not None:
        author_about = ''.join(filter(
            lambda x: x not in filter_chars,
            author_about_info.text
        )).strip()

    return author_born, author_about


if __name__ == '__main__':
    pages_scraped = 0
    df = []
    next_page = BASE_PAGE
    while pages_scraped < 10:
        response = requests.get(next_page)
        soup = bs4.BeautifulSoup(response.text, 'html.parser')
        quote_tiles = soup.find_all('div', {'class': 'quote'})
        for qoute in quote_tiles:
            row = {
                'text': qoute.select_one('span.text').text[1:-1],
                'author': qoute.select_one('small.author').text,
            }
            for df_row in df:
                if df_row['author'] == row['author']:
                    row['author_about'] = df_row['author_about']
                    row['author_born'] = df_row['author_born']
                    break
            else:
                author_url = BASE_PAGE + qoute.select_one('a')['href']
                print(author_url)
                author_data = process_author(author_url)
                row['author_about'] = author_data[1]
                row['author_born'] = author_data[0]
            print(row['author'], row['author_born'], row['text'])
            df.append(row)
        try:
            next_page_placeholder = soup.find_all('li', {'class': 'next'})[0]
            next_page_href = next_page_placeholder.select_one('a')['href']
            next_page = BASE_PAGE + next_page_href
        except IndexError:
            print('THE END')
        pages_scraped += 1
        print(f'PAGES SCRAPED {pages_scraped} ------------------------------')

    with open(Path(BASE_DIR, 'quotes.csv'), 'w', encoding='utf-8') as file:
        print('text|author|author_about|author_born', file=file)
        for row in df:
            print('|'.join(value for value in row.values()),
                  file=file, end='\n')
