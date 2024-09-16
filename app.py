from pathlib import Path

import requests
from flask import Flask, render_template, jsonify, request

from config import DICT_API_KEY, DICT_ENDPOINT, AUDIO_ENDPOINT

app = Flask(__name__)
books_dir = Path('books')


@app.get('/')
def home():

    return render_template('home.html')


@app.get('/<book_name>/<chapter_file>')
def chapter(book_name: str, chapter_file: str):
    content = books_dir.joinpath(book_name).joinpath(chapter_file).read_text()
    return render_template('chapter.html', content=content)


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
    params = {
        'pronunciation_id': pronunciation_id
    }
    response = requests.get(headers=headers, url=AUDIO_ENDPOINT, params=params)

    return response.content


if __name__ == '__main__':
    app.run()
