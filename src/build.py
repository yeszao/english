import json
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed

from pydantic import BaseModel

from src.config import BOOKS_GENERATED_DIR, BOOKS_DIR
from src.utils.book_utils import get_book_objects, Book, get_chapters, Chapter
from src.utils.chapter_utils import tagged_html


class Summary(BaseModel):
    word_count: int
    vocabulary_total: int
    word_count_distribution: dict
    vocabulary_distribution: dict


class BookSummary(BaseModel):
    word_count: int
    sentence_total: int
    sentence_distribution: dict
    vocabulary_total: int
    vocabulary_distribution: dict


def prepare_root_dir():
    shutil.rmtree(BOOKS_GENERATED_DIR, ignore_errors=True)
    BOOKS_GENERATED_DIR.mkdir(parents=True, exist_ok=True)


def parse_chapter(chapter, original_content):
    tagged_content, sentences, chapter_vocabulary, chapter_word_count = tagged_html(original_content)
    print(f"chapter #{chapter.no} parsed.")

    return chapter, tagged_content, sentences, chapter_vocabulary, chapter_word_count


def sort_dict_by_key(d: dict) -> dict:
    return dict(sorted(d.items(), key=lambda item: item[0]))


def generate(book: Book) -> (set, int):
    print(f"[[{book.name}]] started.")
    generated_book_dir = BOOKS_GENERATED_DIR.joinpath(book.slug)
    generated_book_dir.mkdir(parents=True, exist_ok=True)

    summary_file = generated_book_dir.joinpath("summary.json")
    vocabulary_file = generated_book_dir.joinpath("vocabulary.txt")
    summary = BookSummary(word_count=0, sentence_total=0, sentence_distribution={}, vocabulary_total=0,
                          vocabulary_distribution={})

    book_vocabulary = set()
    book_word_count = 0
    futures=[]
    with ThreadPoolExecutor() as executor:
        for chapter in get_chapters(book):
            original_content = BOOKS_DIR.joinpath(book.slug).joinpath(chapter.html_file).read_text()
            futures.append(executor.submit(parse_chapter, chapter, original_content))

    for future in as_completed(futures):
        chapter, tagged_content, sentences, chapter_vocabulary, chapter_word_count = future.result()

        tagged_html_file = generated_book_dir.joinpath(chapter.html_file)
        tagged_html_file.write_text(tagged_content)

        sentences_file = generated_book_dir.joinpath(chapter.sentences_file)
        sentences_file.write_text(json.dumps(sentences, ensure_ascii=False, indent=2))

        chapter_vocabulary_file = generated_book_dir.joinpath(chapter.vocabulary_file)
        chapter_vocabulary_file.write_text('\n'.join(sorted(list(chapter_vocabulary))))

        summary.sentence_total += len(sentences)
        summary.sentence_distribution[chapter.no] = len(sentences)
        summary.vocabulary_distribution[chapter.no] = len(chapter_vocabulary)
        book_vocabulary.update(chapter_vocabulary)
        book_word_count += chapter_word_count

    summary.word_count = book_word_count
    summary.vocabulary_total = len(book_vocabulary)
    summary.sentence_distribution = sort_dict_by_key(summary.sentence_distribution)
    summary.vocabulary_distribution = sort_dict_by_key(summary.vocabulary_distribution)
    summary_file.write_text(json.dumps(summary.model_dump(), ensure_ascii=False, indent=2))
    vocabulary_file.write_text('\n'.join(sorted(list(book_vocabulary))))

    print(f"[[{book.name}]] generated.")
    return book_vocabulary, book_word_count


if __name__ == '__main__':
    prepare_root_dir()
    books = get_book_objects()

    summary = Summary(word_count=0, vocabulary_total=0, word_count_distribution={}, vocabulary_distribution={})

    vocabulary = set()
    for b in books:
        book_vocabulary, book_word_count = generate(b)
        summary.word_count += book_word_count
        summary.word_count_distribution[b.slug] = book_word_count
        summary.vocabulary_distribution[b.slug] = len(book_vocabulary)
        vocabulary.update(book_vocabulary)

    summary.vocabulary_total = len(vocabulary)
    summary_file = BOOKS_GENERATED_DIR.joinpath("summary.json")
    summary_file.write_text(json.dumps(summary.model_dump(), ensure_ascii=False, indent=2))
    print("All done!")
