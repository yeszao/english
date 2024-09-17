import io
import os
import tempfile
from pathlib import Path
import re
from bs4 import BeautifulSoup
import requests
from flask import Flask, render_template, jsonify, request, url_for, send_file
from pydub import AudioSegment

from config import DICT_API_KEY, DICT_ENDPOINT, AUDIO_ENDPOINT

app = Flask(__name__)
books_dir = Path('books')


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
    content = books_dir.joinpath(book_name).joinpath(chapter_file_name).read_text()
    return render_template('chapter.html',
                           book_name=book_name,
                           prev_chapter_url=get_chapter_url(book_name, prev_chapter) if prev_chapter >= 0 else None,
                           next_chapter_url=get_chapter_url(book_name, next_chapter) if next_chapter <= 9 else None,
                           content=transfer_text(content))


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

    # Check if the response is valid and contains MP3 data
    if response.status_code != 200:
        return "Audio file not found", 404

    # Convert the MP3 content to a file-like object
    mp3_audio = io.BytesIO(response.content)
    audio = AudioSegment.from_mp3(mp3_audio)
    m4a_buffer = io.BytesIO()
    audio.export(m4a_buffer, format="mp4")

    # Seek to the beginning of the buffer so it can be read
    m4a_buffer.seek(0)

    # Serve the M4A file directly from memory
    return send_file(m4a_buffer, mimetype='audio/mp4', as_attachment=False, download_name="audio.m4a")


def transfer_text(input_html: str):
    def wrap_words(text):
        # Use regex to split by words and punctuation, keeping them separate
        tokens = re.findall(r"\w+|[^\w\s]|\s+", text, re.UNICODE)

        # Wrap each word in <span class="word">
        wrapped = ''.join([f'<span class="word">{token}</span>' if re.match(r"\w+", token) else token for token in tokens])

        return wrapped

    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(input_html, 'html.parser')

    # Iterate over each paragraph or text-containing tag
    for tag in soup.find_all(['p', 'span']):
        # Replace the content of each tag with the wrapped version
        if tag.string:
            tag.string.replace_with(BeautifulSoup(wrap_words(tag.string), 'html.parser'))

    return str(soup)


if __name__ == '__main__':
    app.run()
