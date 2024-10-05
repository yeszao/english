from typing import List, Set
import spacy
from bs4 import BeautifulSoup
from spacy.language import Language

nlp: Language = spacy.load("en_core_web_sm")


def _get_sentences(text: str) -> List[str]:
    doc = nlp(text)
    return [sent.text for sent in doc.sents]


def _get_words(text: str):
    return nlp(text)


def tagged_html(input_html: str) -> (str, List[str], Set[str]):
    soup = BeautifulSoup(input_html, 'html.parser')

    all_sentences = []
    sentence_no = 0
    all_words = set()
    for tag in soup.find_all(['p', 'span', 'li']):
        sentence_no, sentences = _process_tag(tag, sentence_no, all_words)
        all_sentences.extend(sentences)

    return str(soup), all_sentences, all_words


def _process_tag(tag, sentence_no, all_words) -> (int, List[str]):
    raw_sentences = []
    plain_text = tag.get_text().strip()
    if plain_text.strip() == '':
        return sentence_no, raw_sentences

    sentences = _get_sentences(plain_text)
    raw_sentences.extend(sentences)
    tagged_sentences = []
    for s in sentences:
        sentence_no += 1
        wrapped, words = wrap_words(s)
        all_words.update(words)
        tagged_sentences.append(f'<b><s id="{sentence_no}">{sentence_no}</s>{wrapped}</b> ')

    tag.clear()
    tag.append(BeautifulSoup(' '.join(tagged_sentences), 'html.parser'))

    return sentence_no, raw_sentences


def wrap_words(text, start_tag='<i>', end_tag='</i>') -> (str, int):
    doc = _get_words(text)
    wrapped = ''
    words = set()

    for token in doc:
        if token.is_alpha:
            words.add(token.text)
            wrapped += f'{start_tag}{token.text}{end_tag}'
        else:
            # Keep punctuation and non-alpha tokens unchanged
            wrapped += token.text

        if token.whitespace_:
            wrapped += token.whitespace_

    return wrapped, words


def wrap_words_and_entities(text, start_tag='<i>', end_tag='</i>'):
    doc = _get_words(text)
    wrapped = ''

    # Merge entities (such as "New York" or "John Smith") into single tokens
    with doc.retokenize() as retokenizer:
        for ent in doc.ents:
            retokenizer.merge(ent)

    for token in doc:
        if token.is_alpha or token.ent_type_:
            wrapped += f'{start_tag}{token.text}{end_tag}'
        else:
            # Keep punctuation and non-alpha tokens unchanged
            wrapped += token.text

        if token.whitespace_:
            wrapped += token.whitespace_

    return wrapped
