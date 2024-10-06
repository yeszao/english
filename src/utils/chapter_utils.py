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
    all_vocabulary = set()
    all_word_count = 0
    for tag in soup.find_all(['p', 'span', 'li']):
        sentence_no, sentences, sentence_word_count = _process_tag(tag, sentence_no, all_vocabulary)
        all_word_count += sentence_word_count
        all_sentences.extend(sentences)

    return str(soup), all_sentences, all_vocabulary, all_word_count


def _process_tag(tag, sentence_no, all_vocabulary) -> (int, List[str], int):
    raw_sentences = []
    plain_text = tag.get_text().strip()
    if plain_text.strip() == '':
        return sentence_no, raw_sentences

    sentences = _get_sentences(plain_text)
    raw_sentences.extend(sentences)
    tagged_sentences = []
    sentence_word_count = 0

    for s in sentences:
        sentence_no += 1
        wrapped, vocabulary, word_count = wrap_words(s)
        all_vocabulary.update(vocabulary)
        sentence_word_count += word_count
        tagged_sentences.append(f'<b><s id="{sentence_no}">{sentence_no}</s>{wrapped}</b> ')

    tag.clear()
    tag.append(BeautifulSoup(' '.join(tagged_sentences), 'html.parser'))

    return sentence_no, raw_sentences, sentence_word_count


def wrap_words(text, start_tag='<i>', end_tag='</i>') -> (str, int, int):
    doc = _get_words(text)
    wrapped = ''
    vocabulary = set()
    word_count = 0

    for token in doc:
        if token.is_alpha:
            vocabulary.add(token.text.lower())
            word_count += 1
            wrapped += f'{start_tag}{token.text}{end_tag}'
        else:
            # Keep punctuation and non-alpha tokens unchanged
            wrapped += token.text

        if token.whitespace_:
            wrapped += token.whitespace_

    return wrapped, vocabulary, word_count


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
