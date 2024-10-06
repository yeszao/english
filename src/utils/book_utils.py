import json
from dataclasses import dataclass
from typing import List, Dict

from flask import url_for

from src.config import BOOKS_DIR


@dataclass
class Book:
    id: int
    author: str
    name: str
    slug: str
    chapter_number: int
    cover: str
    description: str


@dataclass
class Chapter:
    no: int
    title: str
    html_file: str
    sentences_file: str
    vocabulary_file:str

    def __init__(self, no):
        self.no = no
        self.title = f"Chapter {no}"
        self.html_file = f"{no}.html"
        self.sentences_file = f"{no}.json"
        self.vocabulary_file = f"{no}.txt"

    def get_url(self, book_slug: str) -> str:
        return generate_chapter_url(book_slug, self.no)


def get_chapters(book: Book) -> List[Chapter]:
    return [Chapter(i) for i in range(1, book.chapter_number + 1)]


def get_prev_next_chapter_urls(book: Book, chapter_no: int) -> (str, str):
    prev_chapter = chapter_no - 1
    next_chapter = chapter_no + 1
    prev_chapter_url = generate_chapter_url(book.slug, prev_chapter) if prev_chapter >= 0 else None
    next_chapter_url = generate_chapter_url(book.slug, next_chapter) if next_chapter <= book.chapter_number else None
    return prev_chapter_url, next_chapter_url


def generate_chapter_url(book_slug: str, chapter_no: int) -> str:
    return url_for('get_chapter', book_slug=book_slug, chapter_no=chapter_no)


def get_book_objects() -> List[Book]:
    return [Book(**item) for item in get_book_dicts()]


def get_book_dicts():
    return json.loads(BOOKS_DIR.joinpath("books.json").read_text())


def get_book_slug_map() -> Dict[str, Book]:
    return {book.slug: book for book in get_book_objects()}
