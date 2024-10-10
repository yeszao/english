import pytest

from src.utils.google_news_utils import parse_cnn, parse_bbc
from tests import TEST_FILES_DIR


def test_parse_cnn():
    input_file = TEST_FILES_DIR.joinpath("news").joinpath('cnn.html')
    input_html = input_file.read_text()
    content_html = parse_cnn(input_html)
    assert "I can continue chasing that" in content_html
    assert "At the end of the day, we’re doing this for them" in content_html


@pytest.mark.parametrize("segment", [
    '<img src="https://ichef.bbci.co.uk/news/480/cpsprodpb/8347/live/87c5d670-84c8-11ef-83dd-fbf1b9732cf0.jpg.webp"/>',
    "A former Met Police officer has been charged with eight sexual offences against two women.",
    "The 49-year-old will appear at Westminster Magistrates' Court on 17 October.",
    " He said: \"The charges come in the wake of an extensive and complex investigation conducted over a period of several months.\"",
])
def test_parse_bbc(segment: str):
    input_file = TEST_FILES_DIR.joinpath("news").joinpath('bbc.html')
    input_html = input_file.read_text()
    content_html = parse_bbc(input_html)
    assert segment in content_html
    assert 'Sign up for our Politics Essential newsletter' not in content_html


@pytest.mark.parametrize("segment", [
    'US officials have warned of the threat to life posed by Hurricane Milton,',
    'Milton is still packing ferocious winds of up to 155mph (250km/h)',
    "Long queues at petrol stations began forming in south Florida, with some reports of stations running out of fuel.",
    "Where and when Milton is expected to hit",
])
def test_parse_bbc2(segment: str):
    input_file = TEST_FILES_DIR.joinpath("news").joinpath('bbc2.html')
    input_html = input_file.read_text()
    content_html = parse_bbc(input_html)
    assert segment in content_html
    assert 'Sign up for our Politics Essential newsletter' not in content_html


@pytest.mark.parametrize("segment", [
    'https://ichef.bbci.co.uk/news/480/cpsprodpb/dc21/live/beba2660-1e8c-11ef-80aa-699d54c46324.jpg.webp',
    'for more than two decades. Its annual revenues are in excess of $100bn (£76.5bn).',
    'During his tenure the group made many bold acquisitions, among them the takeover of Anglo-Dutch steelmaker Corus and UK-based car brands Jaguar and Land Rover. Some',
    " Mumbai terror attacks",
    "a few months after the previous incumbent, Cyrus Mistry, was ousted, sparking a bitter",
    "\"In a country like ours,\" he said, \"you have to try and lead by example, not flaunt your wealth and prominence.\"",
])
def test_parse_bbc3(segment: str):
    input_file = TEST_FILES_DIR.joinpath("news").joinpath('bbc3.html')
    input_html = input_file.read_text()
    content_html = parse_bbc(input_html)
    assert segment in content_html
    assert 'Sign up for our Politics Essential newsletter' not in content_html
