from src.db.entity import News
from src.utils.chapter_utils import tagged_html
from src.utils.google_news_utils import get_cnn_html, parse_cnn, get_bbc_html, parse_bbc, get_response
from src.db.news_dao import NewsDao

publications = [
    {
        "name": "CNN",
        "publication_token": "CAAqBwgKMKHL9QowkqbaAg",
        "section_token": "CAQqEAgAKgcICjChy_UKMJKm2gIw-9OmBQ",
        "html_getter": get_cnn_html,
        "parser": parse_cnn,
    },
    {
        "name": "BBC",
        "publication_token": "CAAqKQgKIiNDQklTRkFnTWFoQUtEbUppWXk1amJ5NTFheTl1WlhkektBQVAB",
        "section_token": "",
        "html_getter": get_bbc_html,
        "parser": parse_bbc,
    }
]


if __name__ == '__main__':
    for p in publications:
        response = get_response(p)
        url, html = p['html_getter'](response['news_results'])
        title, content = p['parser'](html)
        tagged_content, sentences, vocabulary, word_count = tagged_html(content)
        tagged_title, _, _, _ = tagged_html("<h1>" + title + "</h1>")

        news = News(
            url=url,
            publication=p['name'],
            title=title,
            tagged_title=tagged_title,
            content_html=content,
            tagged_content_html=tagged_content,
            vocabulary_count=len(vocabulary),
            word_count=word_count,
            sentences='\n'.join(sentences),
            vocabulary='\n'.join(sorted(list(vocabulary))),
        )

        NewsDao.add_one(news)
        print(f"Saved [{p['name']}] {url}")
