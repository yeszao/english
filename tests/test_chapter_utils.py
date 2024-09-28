import pytest

from src.utils.chapter_utils import tagged_html, wrap_words
from tests import TEST_FILES_DIR

input_file = TEST_FILES_DIR.joinpath("chapter_utils").joinpath('chapter.html')


def test_tagged_html():
    input_html = input_file.read_text()
    tagged_content, sentences = tagged_html(input_html)
    assert len(sentences) == 14
    assert len(tagged_content) > 0
    assert 'callMontauk' not in tagged_content


@pytest.mark.parametrize("text, expected", [
    ("Hello, world!", '[Hello], [world]!'),
    ("John Smith was born in New York but moved to Los Angeles in United States.", '[John Smith] [was] [born] [in] [New York] [but] [moved] [to] [Los Angeles] [in] [United States].'),
])
def test_wrap_words(text, expected):
    assert wrap_words(text, '[', ']') == expected
