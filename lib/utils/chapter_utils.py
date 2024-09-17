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


def transfer_text(input_html: str):
    def wrap_words(text):
        # Use regex to split by words and punctuation, keeping them separate
        doc = get_words(text)

        wrapped = ''
        for token in doc:
            wrapped += f'<span class="word">{token.text}</span>' if token.is_alpha else token.text
            if token.whitespace_:
                wrapped += token.whitespace_

        return wrapped

    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(input_html, 'html.parser')

    # Iterate over each paragraph or text-containing tag
    for tag in soup.find_all(['p', 'span']):
        # Replace the content of each tag with the wrapped version
        if tag.string:
            sentences = get_sentences(str(tag.string).strip())
            new_sentences = []
            # add a span tag for each sentence
            for s in sentences:
                new_sentences.append(f'<span class="sentence">{wrap_words(s)}</span> ')

            tag.string.replace_with(BeautifulSoup(' '.join(new_sentences), 'html.parser'))

    return str(soup)
