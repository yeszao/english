from src.utils.google_news_utils import parse_cnn, parse_bbc
from tests import TEST_FILES_DIR


def test_parse_cnn():
    input_file = TEST_FILES_DIR.joinpath("news").joinpath('cnn.html')
    input_html = input_file.read_text()
    title, content, html = parse_cnn(input_html)
    assert title == 'Why Rema decided 2024 was the year to rep his city'
    assert "I can continue chasing that" in content
    assert "At the end of the day, we’re doing this for them" in content


def test_parse_bbc():
    input_file = TEST_FILES_DIR.joinpath("news").joinpath('bbc.html')
    input_html = input_file.read_text()
    title, content, html = parse_bbc(input_html)
    assert title == 'Ex-Met PC David Carrick charged with sexual offences'
    assert "David Carrick from Stevenage, Hertfordshire," in content
    assert "Det Ch Insp Iain Moor, from Hertfordshire" in content


def test_parse_bbc2():
    input_file = TEST_FILES_DIR.joinpath("news").joinpath('bbc2.html')
    input_html = input_file.read_text()
    title, content, html = parse_bbc(input_html)
    assert title == "Florida warned of 'potentially catastrophic' Hurricane Milton impact"
    assert "Milton is still packing ferocious winds of up to 155mph" in content
    assert "Long queues at petrol stations began forming in south Florida, with some reports of stations running out of fuel." in content

