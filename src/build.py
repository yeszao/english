import json
import shutil
from pathlib import Path

from src.config import BOOKS_GENERATED_DIR, BOOKS_DIR, TAGGED_HTML_DIRNAME, SENTENCES_DIRNAME
from src.utils.book_utils import get_book_objects, Book, get_chapters
from src.utils.chapter_utils import tagged_html


def prepare_root_dir():
    shutil.rmtree(BOOKS_GENERATED_DIR, ignore_errors=True)
    BOOKS_GENERATED_DIR.mkdir(parents=True, exist_ok=True)


def _get_dirs(book: Book) -> (Path, Path):
    tagged_dir = BOOKS_GENERATED_DIR.joinpath(book.slug).joinpath(TAGGED_HTML_DIRNAME)
    tagged_dir.mkdir(parents=True, exist_ok=True)

    sentences_dir = BOOKS_GENERATED_DIR.joinpath(book.slug).joinpath(SENTENCES_DIRNAME)
    sentences_dir.mkdir(parents=True, exist_ok=True)

    return tagged_dir, sentences_dir


def generate(book: Book):
    tagged_dir, sentences_dir = _get_dirs(book)
    for chapter in get_chapters(book):
        original_content = BOOKS_DIR.joinpath(book.slug).joinpath(chapter.html_file).read_text()
        tagged_content, sentences = tagged_html(original_content)

        tagged_html_file = tagged_dir.joinpath(chapter.html_file)
        tagged_html_file.write_text(tagged_content)

        sentences_file = sentences_dir.joinpath(chapter.sentences_file)
        sentences_file.write_text(json.dumps(sentences, ensure_ascii=False, indent=2))

        print(f"Generated <<{book.name}>> chapter #{chapter.no} [{chapter.no/book.chapter_number*100:.0f}%]")


if __name__ == '__main__':
    prepare_root_dir()
    books = get_book_objects()
    for b in books:
        generate(b)

    print("All done!")
