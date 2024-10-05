import json
import shutil
import threading

from pydantic import BaseModel

from src.config import BOOKS_GENERATED_DIR, BOOKS_DIR
from src.utils.book_utils import get_book_objects, Book, get_chapters
from src.utils.chapter_utils import tagged_html


class Summary(BaseModel):
    sentence_total: int
    sentence_distribution: dict
    word_total: int
    word_distribution: dict


def prepare_root_dir():
    shutil.rmtree(BOOKS_GENERATED_DIR, ignore_errors=True)
    BOOKS_GENERATED_DIR.mkdir(parents=True, exist_ok=True)


def generate(book: Book):
    generated_book_dir = BOOKS_GENERATED_DIR.joinpath(book.slug)
    generated_book_dir.mkdir(parents=True, exist_ok=True)

    summary_file = generated_book_dir.joinpath("summary.json")
    words_file = generated_book_dir.joinpath("words.json")
    summary = Summary(sentence_total=0, sentence_distribution={}, word_total=0, word_distribution={})

    book_words = set()
    for chapter in get_chapters(book):
        original_content = BOOKS_DIR.joinpath(book.slug).joinpath(chapter.html_file).read_text()
        tagged_content, sentences, chapter_words = tagged_html(original_content)

        tagged_html_file = generated_book_dir.joinpath(chapter.html_file)
        tagged_html_file.write_text(tagged_content)

        sentences_file = generated_book_dir.joinpath(chapter.sentences_file)
        sentences_file.write_text(json.dumps(sentences, ensure_ascii=False, indent=2))

        summary.sentence_total += len(sentences)
        summary.sentence_distribution[chapter.no] = len(sentences)
        summary.word_distribution[chapter.no] = len(chapter_words)
        book_words.update(chapter_words)

        print(f"Generated <<{book.name}>> chapter #{chapter.no} [{chapter.no/book.chapter_number*100:.0f}%]")

    summary.word_total = len(book_words)
    summary_file.write_text(json.dumps(summary.model_dump(), ensure_ascii=False, indent=2))
    words_file.write_text(json.dumps(sorted(list(book_words)), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    prepare_root_dir()
    books = get_book_objects()

    threads = []
    for b in books:
        thread = threading.Thread(target=generate, args=(b,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print("All done!")
