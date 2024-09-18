from lib.utils.chapter_utils import tagged_html
from tests import TEST_FILES_DIR

input_file = TEST_FILES_DIR.joinpath("chapter_utils").joinpath('chapter.html')


def test_tagged_html():
    input_html = input_file.read_text()
    tagged_content, sentences = tagged_html(input_html)
    assert len(sentences) == 14
    assert len(tagged_content) > 0
    assert 'callMontauk' not in tagged_content


