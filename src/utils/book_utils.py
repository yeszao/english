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


def get_chapter_urls(book: Book, chapter_no: int) -> (str, str):
    prev_chapter = chapter_no - 1
    next_chapter = chapter_no + 1
    prev_chapter_url = generate_chapter_url(book.slug, prev_chapter) if prev_chapter >= 0 else None
    next_chapter_url = generate_chapter_url(book.slug, next_chapter) if next_chapter <= book.chapter_number else None
    return prev_chapter_url, next_chapter_url


def generate_chapter_url(book_slug: str, chapter_no: int) -> str:
    return url_for('chapter', book_slug=book_slug, chapter_no=chapter_no)


def get_book_objects() -> List[Book]:
    return [Book(**item) for item in get_book_dicts()]


def get_book_dicts():
    return json.loads(BOOKS_DIR.joinpath("books.json").read_text())


def get_book_slug_map() -> Dict[str, Book]:
    return {book.slug: book for book in get_book_objects()}
