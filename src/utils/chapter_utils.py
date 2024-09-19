from typing import List
import spacy
from bs4 import BeautifulSoup
from spacy.language import Language

nlp: Language = spacy.load("en_core_web_sm")


def get_sentences(text: str) -> List[str]:
    doc = nlp(text)
    return [sent.text for sent in doc.sents]


def get_words(text: str):
    return nlp(text)


def tagged_html(input_html: str) -> (str, List[str]):
    soup = BeautifulSoup(input_html, 'html.parser')

    all_sentences = []
    sentence_no = 0
    for tag in soup.find_all(['p', 'span', 'li']):
        sentence_no, sentences = process_tag(tag, sentence_no)
        all_sentences.extend(sentences)

    return str(soup), all_sentences


def process_tag(tag, sentence_no) -> (int, List[str]):
    raw_sentences = []
    plain_text = tag.get_text().strip()
    if plain_text.strip() == '':
        return sentence_no, raw_sentences

    sentences = get_sentences(plain_text)
    raw_sentences.extend(sentences)
    tagged_sentences = []
    for s in sentences:
        sentence_no += 1
        tagged_sentences.append(f'<span class="sentence"><i class="more" data-no={sentence_no}></i>{wrap_words(s)}</span> ')

    tag.clear()
    tag.append(BeautifulSoup(' '.join(tagged_sentences), 'html.parser'))

    return sentence_no, raw_sentences


def wrap_words(text):
    doc = get_words(text)
    wrapped = ''
    for token in doc:
        wrapped += f'<span class="word">{token.text}</span>' if token.is_alpha else token.text
        if token.whitespace_:
            wrapped += token.whitespace_

    return wrapped
