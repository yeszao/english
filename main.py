from pathlib import Path
import requests
from flask import Flask, render_template, jsonify, request, url_for, Response, stream_with_context

from config import DICT_API_KEY, DICT_ENDPOINT, AUDIO_ENDPOINT
from lib.utils.chapter_utils import transfer_text

app = Flask(__name__)
books_dir = Path('books')
cache_dir = Path('cache')


@app.get('/')
def home():
    return render_template('home.html', book_name='the-great-gatsby')


def get_chapter_url(book_name: str, chapter_num: int) -> str:
    return url_for('chapter', book_name=book_name, chapter_num=str(chapter_num).zfill(2))


@app.get('/book/<book_name>/chapter-<chapter_num>.html')
def chapter(book_name: str, chapter_num: str):
    prev_chapter = int(chapter_num) - 1
    next_chapter = int(chapter_num) + 1
    chapter_file_name = f'chapter-{chapter_num}.html'
    cache_file = cache_dir.joinpath(book_name).joinpath(chapter_file_name)
    if not cache_file.exists():
        content = books_dir.joinpath(book_name).joinpath(chapter_file_name).read_text()
        cache_file.parent.mkdir(parents=True, exist_ok=True)
        tagged_content = transfer_text(content)
        cache_file.write_text(tagged_content)
    else:
        tagged_content = cache_file.read_text()

    return render_template('chapter.html',
                           book_name=book_name,
                           prev_chapter_url=get_chapter_url(book_name, prev_chapter) if prev_chapter >= 0 else None,
                           next_chapter_url=get_chapter_url(book_name, next_chapter) if next_chapter <= 9 else None,
                           content=tagged_content)


@app.get('/translate')
def translate():
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
