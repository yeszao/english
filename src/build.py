import json
import shutil
import threading

from pydantic import BaseModel

from src.config import BOOKS_GENERATED_DIR, BOOKS_DIR
from src.utils.book_utils import get_book_objects, Book, get_chapters
from src.utils.chapter_utils import tagged_html


class Summary(BaseModel):
    word_count: int
    sentence_total: int
    sentence_distribution: dict
    vocabulary_total: int
    vocabulary_distribution: dict


def prepare_root_dir():
    shutil.rmtree(BOOKS_GENERATED_DIR, ignore_errors=True)
    BOOKS_GENERATED_DIR.mkdir(parents=True, exist_ok=True)


def generate(book: Book):
    generated_book_dir = BOOKS_GENERATED_DIR.joinpath(book.slug)
    generated_book_dir.mkdir(parents=True, exist_ok=True)

    summary_file = generated_book_dir.joinpath("summary.json")
    vocabulary_file = generated_book_dir.joinpath("vocabulary.txt")
    summary = Summary(word_count =0, sentence_total=0, sentence_distribution={}, vocabulary_total=0, vocabulary_distribution={})

    book_words = set()
    word_count = 0
    for chapter in get_chapters(book):
        original_content = BOOKS_DIR.joinpath(book.slug).joinpath(chapter.html_file).read_text()
        tagged_content, sentences, chapter_vocabulary, chapter_word_count = tagged_html(original_content)

        tagged_html_file = generated_book_dir.joinpath(chapter.html_file)
        tagged_html_file.write_text(tagged_content)

        sentences_file = generated_book_dir.joinpath(chapter.sentences_file)
        sentences_file.write_text(json.dumps(sentences, ensure_ascii=False, indent=2))

        chapter_vocabulary_file = generated_book_dir.joinpath(chapter.vocabulary_file)
        chapter_vocabulary_file.write_text('\n'.join(sorted(list(chapter_vocabulary))))

        summary.sentence_total += len(sentences)
        summary.sentence_distribution[chapter.no] = len(sentences)
        summary.vocabulary_distribution[chapter.no] = len(chapter_vocabulary)
        book_words.update(chapter_vocabulary)
        word_count += chapter_word_count

        print(f"Generated <<{book.name}>> chapter #{chapter.no} [{chapter.no/book.chapter_number*100:.0f}%]")

    summary.word_count = word_count
    summary.vocabulary_total = len(book_words)
    summary_file.write_text(json.dumps(summary.model_dump(), ensure_ascii=False, indent=2))
    vocabulary_file.write_text('\n'.join(sorted(list(book_words))))


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
