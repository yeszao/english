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


def get_response(publication: dict):
    url = "https://serpapi.com/search"
    params = {
        "api_key": SERPAPI_KEY,
        "engine": "google_news",
        "gl": "us",
        "hl": "en",
        "publication_token": publication["publication_token"],
    }

    if publication["section_token"]:
        params["section_token"] = publication["section_token"]

    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def get_html(url):
    response = requests.get(url, headers=headers)
    return response.text


def get_cnn_html(news_results) -> (str, str):
    url = ''
    for r in news_results:
        if '/video/' not in r['link']:
            url = r['link']
            break

    return url, get_html(url)


def parse_cnn(html: str):
    if not html:
        return None

    tree = etree.fromstring(html, etree.HTMLParser())
    title = tree.xpath("//h1/text()")[0].strip()
    content = tree.xpath('//div[@class="article__content"]')[0]
    soup = BeautifulSoup(etree.tostring(content), 'html.parser')

    tags = soup.find_all(['p', 'img'])

    clean_attr(tags)
    content_html = ''.join(str(tag) for tag in tags)

    return title, content_html


def get_bbc_html(news_results) -> (str, str):
    url = ''
    for r in news_results:
        if '/news/' in r['link']:
            url = r['link']
            break

    return url, get_html(url)


def parse_bbc(html: str):
    if not html:
        return None

    tree = etree.fromstring(html, etree.HTMLParser())
    if tree.xpath("//h1/text()"):
        title = tree.xpath("//h1/text()")[0].strip()
    elif tree.xpath("//h1/span/text()"):
        title = tree.xpath("//h1/span/text()")[0].strip()
    else:
        print("Title not found")
        return None

    texts = tree.xpath('//article//div[@data-component="text-block"]')
    all_tags = []
    for text in texts[:-1]:
        soup = BeautifulSoup(etree.tostring(text), 'html.parser')
        tags = soup.find_all(['p', 'img'])
        all_tags.extend(tags)

    clean_attr(all_tags)
    content_html = ''.join(str(tag) for tag in all_tags)
    return title, content_html


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

