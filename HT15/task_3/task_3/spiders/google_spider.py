import bs4
import re
import scrapy
from scrapy.http.response.xml import XmlResponse


class GoogleSpiderSpider(scrapy.Spider):
    name = 'google_spider'
    allowed_domains = [
        'chrome.google.com',
        'https://chromewebstore.google.com',
    ]
    start_urls = ['https://chrome.google.com/webstore/sitemap']

    def parse(self, response: XmlResponse):
        soup = bs4.BeautifulSoup(response._body, 'xml')
        shards = soup.select('sitemap loc')
        for shard in shards:
            yield response.follow(shard.text, callback=self.parse_shard)

    def parse_shard(self, response):
        soup = bs4.BeautifulSoup(response._body, 'xml')
        pages = soup.select('loc')
        for page in pages:
            yield response.follow(page.text, callback=self.parse_page)

    def parse_page(self, response: XmlResponse):
        soup = bs4.BeautifulSoup(response._body, 'html.parser')
        short_info_selector = soup.select_one('div[itemprop="description"]')
        short_info_text = ''
        if short_info_selector:
            short_info_text = str(short_info_selector.text)
        short_info_text = re.sub(r'(\,|\W+)', ' ', short_info_text)
        title_selector = soup.select_one('h1')
        title_text = title_selector.text if title_selector else ''
        addon_id = response.url.split('?')[0].rsplit('/', 1)[1]
        yield {
            'addon_id': addon_id,
            'addon_title': title_text,
            'addon_short_info': short_info_text
        }
