from lxml import etree
import requests
from bs4 import BeautifulSoup

from src.config import SERPAPI_KEY
from src.utils.openai_translator_utils import ChatGptTranslator

translater = ChatGptTranslator()

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "referer": "https://news.google.com/",
}


def get_google_news():
    url = "https://serpapi.com/search"
    params = {
        "api_key": SERPAPI_KEY,
        "engine": "google_news",
        "gl": "us",
        "hl": "en",
        "topic_token": "CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx1YlY4U0FtVnVHZ0pWVXlnQVAB",  # world news
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def get_html(url) -> str:
    return requests.get(url, headers=headers).text


def check_url(r: dict) -> str:
    black_uri = ('/live/', '/live-news/', '/video/')
    link = r['highlight']['link']
    return link if not any(uri in link for uri in black_uri) else None


def parse_cnn(html: str) -> str:
    if not html:
        return ''

    tree = etree.fromstring(html, etree.HTMLParser())
    content = tree.xpath('//div[@class="article__content"]')[0]
    soup = BeautifulSoup(etree.tostring(content), 'html.parser')
    tags = soup.find_all(['p', 'img'])

    clean_attr(tags)
    return ''.join(str(tag) for tag in tags)


def parse_bbc(html: str) -> str:
    if not html:
        return ''

    tree = etree.fromstring(html, etree.HTMLParser())
    texts = tree.xpath('//article//div[@data-component="text-block"]')
    all_tags = []
    for text in texts[:-1]:
        soup = BeautifulSoup(etree.tostring(text), 'html.parser')
        tags = soup.find_all(['p', 'img'])
        all_tags.extend(tags)

    clean_attr(all_tags)
    return ''.join(str(tag) for tag in all_tags)


def clean_attr(tags: list):
    for tag in tags:
        if tag.name == 'p':
            tag.attrs = {}
            for sub_tag in tag.find_all():
                if sub_tag.name == 'a':
                    sub_tag.attrs = {'href': sub_tag.get('href'), 'target': '_blank', 'rel': 'nofollow'}
                elif sub_tag.name == 'b':
                    sub_tag.unwrap()
                else:
                    sub_tag.attrs = {}
        elif tag.name == 'img':
            tag.attrs = {'src':  tag.get('src')}

