import json
import logging

from src.config import CACHE_DIR, LOG_DIR
from src.db.entity import News
from src.utils.chapter_utils import tagged_html
from src.utils.date_utils import get_now_filename, str_to_datetime
from src.utils.google_news_utils import parse_cnn, parse_bbc, get_google_news, check_url, get_html
from src.db.news_dao import NewsDao
from src.utils.logging_utils import init_logging

publications = {
    "CNN": {
        "name": "CNN",
        "html_parser": parse_cnn,
    },
    "BBC.com": {
        "name": "BBC",
        "html_parser": parse_bbc,
    }
}

if __name__ == '__main__':
    init_logging(LOG_DIR.joinpath("crawl_news.log"))
    news_results = get_google_news()
    CACHE_DIR.joinpath("news").mkdir(parents=True, exist_ok=True)
    CACHE_DIR.joinpath("news").joinpath(f"{get_now_filename()}.json").write_text(json.dumps(news_results, indent=2))

    for result in news_results['news_results']:
        if 'highlight' not in result:
            continue

        source_name = result['highlight']['source']['name']
        if source_name not in publications:
            continue

        url = check_url(result)
        if not url:
            continue

        if NewsDao.get_by_url(url):
            continue

        html = get_html(url)
        content_html = publications[source_name]['html_parser'](html)
        if not content_html:
            logging.error(f"Failed to get html content from {url}")
            continue

        tagged_content, sentences, vocabulary, word_count = tagged_html(content_html)

        title = result['highlight']['title']
        tagged_title, _, _, _ = tagged_html("<h1>" + title + "</h1>")

        news = News(
            url=url,
            publication=publications[source_name]['name'],
            title=title,
            tagged_title=tagged_title,
            content_html=content_html,
            tagged_content_html=tagged_content,
            vocabulary_count=len(vocabulary),
            word_count=word_count,
            sentences='\n'.join(sentences),
            vocabulary='\n'.join(sorted(list(vocabulary))),
            date=str_to_datetime(result['highlight']['date'])
        )

        NewsDao.add_one(news)
        logging.info(f"Saved [{publications[source_name]['name']}] {url}")
