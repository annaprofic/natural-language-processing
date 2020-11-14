import re
import nltk
import inflect
import unicodedata
from nltk.corpus import stopwords

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('gutenberg')
nltk.download('averaged_perceptron_tagger')

DECILLION = 10 ** 33


def remove_between_square_brackets(text):
    return re.sub(r'\[[^]]*\]', '', text)


def denoise_text(text):
    text = remove_between_square_brackets(text)
    return text


def remove_non_ascii(words):
    """Remove non-ASCII characters from list of tokenized words"""
    new_words = []
    for word in words:
        new_word = unicodedata.normalize('NFKD', word).encode('ascii', 'ignore').decode('utf-8', 'ignore')
        new_words.append(new_word)
    return new_words


def to_lowercase(words):
    """Convert all characters to lowercase from list of tokenized words"""
    new_words = []
    for word in words:
        new_word = word.lower()
        new_words.append(new_word)
    return new_words


def remove_punctuation(words):
    """Remove punctuation from list of tokenized words"""
    new_words = []
    for word in words:
        new_word = re.sub(r'[^\w\s]', '', word)
        if new_word != '':
            new_words.append(new_word)
    return new_words


def replace_numbers(words):
    """Replace all interger occurrences in list of tokenized words with textual representation"""
    p = inflect.engine()
    new_words = []
    for word in words:
        if not word.isdigit():
        #     if int(word) > DECILLION:
        #         continue
        #     new_word = p.number_to_words(word)
        #     new_words.append(new_word)
        # else:
            new_words.append(word)
    return new_words


def remove_stopwords(words):
    """Remove stop words from list of tokenized words"""
    new_words = []
    for word in words:
        if word not in stopwords.words('english'):
            new_words.append(word)
    return new_words


def remove_single_character(words):
    """Remove single-character tokens"""
    new_words = []
    for word in words:
        if len(word) > 1:
            new_words.append(word)
    return new_words



