import pytest

from src.utils.chapter_utils import tagged_html, wrap_words, wrap_words_and_entities
from tests import TEST_FILES_DIR

input_file = TEST_FILES_DIR.joinpath("chapter_utils").joinpath('chapter.html')


def test_tagged_html():
    input_html = input_file.read_text()
    tagged_content, sentences, chapter_words = tagged_html(input_html)
    assert len(sentences) == 14
    assert len(tagged_content) > 0
    assert 'callMontauk' not in tagged_content


@pytest.mark.parametrize("text, expected", [
    ("Hello, world!", ('[Hello], [world]!', 2)),
    ("I love Perter's laptop.", ('[I] [love] [Perter]\'s [laptop].', 4)),
    ("John Smith was born in New York but moved to Los Angeles in United States.", ('[John] [Smith] [was] [born] [in] [New] [York] [but] [moved] [to] [Los] [Angeles] [in] [United] [States].', 14)),
])
def test_wrap_words(text, expected):
    wrapped, words = wrap_words(text, '[', ']')
    assert wrapped, len(words) == expected


@pytest.mark.parametrize("text, expected", [
    ("Hello, world!", '[Hello], [world]!'),
    ("I love Perter's laptop.", '[I] [love] [Perter]\'s [laptop].'),
    ("John Smith was born in New York but moved to Los Angeles in United States.", '[John Smith] [was] [born] [in] [New York] [but] [moved] [to] [Los Angeles] [in] [United States].'),
])
def test_wrap_words_and_entities(text, expected):
    assert wrap_words_and_entities(text, '[', ']') == expected
