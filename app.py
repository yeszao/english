from pathlib import Path

from flask import Flask, render_template

app = Flask(__name__)
books_dir = Path('books')


@app.route('/')
def home():

    return render_template('home.html')


@app.route('/<book_name>/<chapter_file>')
def chapter(book_name: str, chapter_file: str):
    content = books_dir.joinpath(book_name).joinpath(chapter_file).read_text()
    return render_template('chapter.html', content=content)


if __name__ == '__main__':
    app.run()
