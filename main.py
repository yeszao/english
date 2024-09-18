import json
from pathlib import Path
import requests
from flask import Flask, render_template, jsonify, request, url_for, Response, stream_with_context

from config import DICT_API_KEY, DICT_ENDPOINT, AUDIO_ENDPOINT
from lib.utils.chapter_utils import tagged_html
from lib.utils.openai_translator_utils import ChatGptTranslator

app = Flask(__name__)
books_dir = Path('books')
cache_dir = Path('cache')


@app.get('/')
def home():
    return render_template('home.html', books=get_books())


def get_chapter_url(book_slug: str, chapter_no: int) -> str:
    return url_for('chapter', book_slug=book_slug, chapter_no=str(chapter_no))


def get_books():
    return json.loads(books_dir.joinpath("books.json").read_text())


def get_book_slug_map():
    return {book['slug']: book for book in get_books()}


def get_book_id_map():
    return {book['id']: book for book in get_books()}


@app.get('/book/<book_slug>/chapter-<chapter_no>.html')
def chapter(book_slug: str, chapter_no: str):
    prev_chapter = int(chapter_no) - 1
    next_chapter = int(chapter_no) + 1
    chapter_file_name = f'chapter-{chapter_no}.html'
    cache_file = cache_dir.joinpath(book_slug).joinpath("tagged").joinpath(chapter_file_name)
    sentences_file = cache_dir.joinpath(book_slug).joinpath("sentences").joinpath(f"{chapter_no}.json")
    if not cache_file.exists():
        content = books_dir.joinpath(book_slug).joinpath(chapter_file_name).read_text()
        cache_file.parent.mkdir(parents=True, exist_ok=True)
        tagged_content, sentences = tagged_html(content)
        sentences_file.parent.mkdir(parents=True, exist_ok=True)
        sentences_file.write_text(json.dumps(sentences, ensure_ascii=False))
        cache_file.write_text(tagged_content)
    else:
        tagged_content = cache_file.read_text()

    return render_template('chapter.html',
                           book=get_book_slug_map()[book_slug],
                           chapter_no=chapter_no,
                           prev_chapter_url=get_chapter_url(book_slug, prev_chapter) if prev_chapter >= 0 else None,
                           next_chapter_url=get_chapter_url(book_slug, next_chapter) if next_chapter <= 9 else None,
                           content=tagged_content)


@app.get('/dictionary')
def dictionary():
    from_lang = request.args.get('from_lang')
    to_lang = request.args.get('to_lang')
    text = request.args.get('text')

    headers = {
        'Content-Type': 'application/json',
        'X-API-KEY': DICT_API_KEY,
    }
    params = {
        'from_lang': from_lang,
        'to_lang': to_lang,
        'text': text
    }
    response = requests.get(headers=headers, url=DICT_ENDPOINT, params=params)

    return jsonify(response.json())


@app.post('/translate')
def translate():
    book_id = int(request.json.get('book_id'))
    chapter_no = request.json.get('chapter_no')
    sentence_no = request.json.get('sentence_no')
    to_lang = request.json.get('to_lang', "zh-Hans")

    assert chapter_no is not None, "Chapter number is required"
    assert sentence_no is not None, "Sentence number is required"

    book = get_book_id_map()[book_id]
    translator = ChatGptTranslator(book["name"])

    translation_file = cache_dir.joinpath(book["slug"]).joinpath("translations").joinpath(to_lang).joinpath(f"{chapter_no}-{sentence_no}.txt")
    translation_file.parent.mkdir(parents=True, exist_ok=True)
    if translation_file.exists():
        return jsonify({'translation': translation_file.read_text()})

    sentences_file = cache_dir.joinpath(book["slug"]).joinpath("sentences").joinpath(f"{chapter_no}.json")
    sentences = json.loads(sentences_file.read_text())
    text = sentences[int(sentence_no) - 1]
    translation = translator.translate(text, to_lang)
    translation_file.write_text(translation)
    return jsonify({'translation': translation})


@app.get('/play')
def play():
    pronunciation_id = request.args.get('id')

    headers = {
        'Content-Type': 'application/json',
        'X-API-KEY': DICT_API_KEY,
    }
    params = {'pronunciation_id': pronunciation_id}
    response = requests.get(headers=headers, url=AUDIO_ENDPOINT, params=params, stream=True)

    # Check if the response is valid and contains MP3 data
    if response.status_code != 200:
        return "Audio file not found", 404

    def generate():
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                yield chunk

    # Serve the M4A file directly from memory
    return Response(stream_with_context(generate()), content_type='audio/mp3')


if __name__ == '__main__':
    app.run()
