import xml.etree.ElementTree as ET
import requests


def parse_sitemap(url):
    response = requests.get(url)

    if response.status_code == 200:
        root = ET.fromstring(response.content)

        # Extract URLs from <loc> tags
        urls = [loc.text for loc in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]

        return urls
    else:
        print(f"Failed to retrieve sitemap. Status code: {response.status_code}")
        return []


# Example usage:
sitemap_url = 'https://chrome.google.com/webstore/sitemap'
parsed_urls = parse_sitemap(sitemap_url)
print(parsed_urls)
