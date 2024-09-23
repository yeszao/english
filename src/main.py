import json
import requests
from flask import Flask, render_template, jsonify, request, Response, stream_with_context

from src.config import DICT_API_KEY, DICT_ENDPOINT, AUDIO_ENDPOINT, CACHE_DIR, BOOKS_DIR, STATIC_VERSION
from src.languages import SUPPORTED_LANGUAGES
from src.utils.book_utils import get_book_slug_map, get_chapter_urls, get_book_objects, get_book_id_map
from src.utils.chapter_utils import tagged_html
from src.utils.openai_translator_utils import ChatGptTranslator

app = Flask(__name__)


@app.context_processor
def inject_global_variables():
    return dict(
        languages=SUPPORTED_LANGUAGES,
    )


@app.get('/')
def home():
    return render_template('home.html',
                           static_version=STATIC_VERSION,
                           books=get_book_objects()
                           )


@app.get('/book/<book_slug>.html')
def book(book_slug: str):
    book = get_book_slug_map()[book_slug]
    return render_template('book.html',
                           book=book)


@app.get('/book/<book_slug>/chapter-<chapter_no>.html')
def chapter(book_slug: str, chapter_no: str):
    chapter_file_name = f'chapter-{chapter_no}.html'
    cache_file = CACHE_DIR.joinpath(book_slug).joinpath("tagged").joinpath(chapter_file_name)
    sentences_file = CACHE_DIR.joinpath(book_slug).joinpath("sentences").joinpath(f"{chapter_no}.json")
    if not cache_file.exists():
        content = BOOKS_DIR.joinpath(book_slug).joinpath(chapter_file_name).read_text()
        cache_file.parent.mkdir(parents=True, exist_ok=True)
        tagged_content, sentences = tagged_html(content)
        sentences_file.parent.mkdir(parents=True, exist_ok=True)
        sentences_file.write_text(json.dumps(sentences, ensure_ascii=False))
        cache_file.write_text(tagged_content)
    else:
        tagged_content = cache_file.read_text()

    book = get_book_slug_map()[book_slug]
    prev_chapter_url, next_chapter_url = get_chapter_urls(book, int(chapter_no))
    return render_template('chapter.html',
                           book=book,
                           chapter_no=chapter_no,
                           prev_chapter_url=prev_chapter_url,
                           next_chapter_url=next_chapter_url,
                           content=tagged_content)


@app.get('/dictionary')
def dictionary():
    from_lang = request.args.get('from_lang', 'en')
    to_lang = request.args.get('to_lang')
    text = request.args.get('text')

    if to_lang is None:
        return jsonify({'error': 'Language is required'}), 401

    if text is None:
        return jsonify({'error': 'Translate text is required'}), 401

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
    to_lang = request.json.get('to_lang')

    if book_id is None:
        return jsonify({'error': 'Book ID is required'}), 401

    if chapter_no is None:
        return jsonify({'error': 'Chapter number is required'}), 401

    if sentence_no is None:
        return jsonify({'error': 'Sentence number is required'}), 401

    if to_lang is None:
        return jsonify({'error': 'Language is required'}), 401

    book = get_book_id_map()[book_id]
    translator = ChatGptTranslator(book.name)

    translation_file = CACHE_DIR.joinpath(book.slug).joinpath("translations").joinpath(to_lang).joinpath(
        f"{chapter_no}-{sentence_no}.txt")
    translation_file.parent.mkdir(parents=True, exist_ok=True)
    if translation_file.exists():
        return jsonify({'translation': translation_file.read_text()})

    sentences_file = CACHE_DIR.joinpath(book.slug).joinpath("sentences").joinpath(f"{chapter_no}.json")
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
