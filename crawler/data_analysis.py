import nltk
import numpy as np
import text_normalizing
from nltk.probability import FreqDist


def normalize(words):
    words = text_normalizing.remove_non_ascii(words)
    words = text_normalizing.to_lowercase(words)
    words = text_normalizing.remove_punctuation(words)
    words = text_normalizing.replace_numbers(words)
    words = text_normalizing.remove_stopwords(words)
    words = text_normalizing.remove_single_character(words)
    return words


def text_to_words(input_text):
    return normalize(nltk.word_tokenize(input_text))


def text_to_sents(input_text):
    return nltk.sent_tokenize(input_text)


def extract_from_file(to_extract='words'):
    files = [open("output/category_Technology.txt"),
             open("output/category_History.txt"),
             open("output/category_Society.txt"),
             open("output/category_Human_activities.txt")]

    for file in files:
        text = file.read().replace("\n", " ") \
            .replace("__________________________article title__________________________", '') \
            .replace("__________________________content list__________________________", '') \
            .replace("__________________________all content__________________________", '')
        file.close()

        text = text_normalizing.denoise_text(text)

        if to_extract == 'words':
            yield text_to_words(text)
        elif to_extract == 'sents':
            yield text_to_sents(text)


def train_naive_bayes(sentences):
    freq_dist = nltk.ConditionalFreqDist()
    for i in range(len(categories)):
        for word in normalize(nltk.word_tokenize(''.join([sent.lower() for cl, sent in sentences if cl == i]))):
            freq_dist[i][word] += 1
    return freq_dist, [sum(1 for class_, sent in sentences if class_ == category) / len(sentences) for category in
                       range(len(categories))]


def get_category(freq_dist, sentence, *, class_probability=(), alpha=0):
    words_in_category = []
    for category, values in freq_dist.items():
        words_in_category.append(sum(v for k, v in freq_dist[category].items()))

    probability = np.ones(len(class_probability))
    for word in normalize(nltk.word_tokenize(sentence.lower())):
        for i in range(len(probability)):
            probability[i] *= (freq_dist[i][word] + alpha) / \
                              (words_in_category[i] + alpha *
                               len(freq_dist[i]))
            probability[i] *= class_probability[i]

    return np.argmax(probability), probability


def accuracy(freq_dist, class_probs, sentences):
    return sum(1 for class_, query in sentences if
               get_category(freq_dist, query, class_probability=class_probs)[0] == class_) / len(sentences)


def sort_sentences_by_category(sents, category):
    return [(category, sent) for sent in sents]


if __name__ == "__main__":

    categories = ['Technology', 'History', 'Society', 'Human_activities']
    for category, words in zip(categories, extract_from_file('words')):
        fdist = FreqDist(words)
        fdist.plot(50, title=category.upper() + ' (WITHOUT NUMBERS)')

    sentences = list()
    for category, sents in zip(categories, extract_from_file('sents')):
        sentences += sort_sentences_by_category(sents, categories.index(category))

    freq_dist, class_probs = train_naive_bayes(sentences)

    freq_words_technology = [word for word, _ in freq_dist[0].most_common(int(len(freq_dist[0]) * 0.15))]
    half_freq_words_technology = [word for word, _ in freq_dist[0].most_common(int(len(freq_dist[0]) * 0.5)) if
                                  word not in freq_words_technology]

    accuracy_for_freq_words = accuracy(freq_dist, class_probs, [(0, word) for word in freq_words_technology])
    accuracy_for_half_freq_words = accuracy(freq_dist, class_probs, [(0, word) for word in half_freq_words_technology])

    print(accuracy_for_freq_words)
    print(accuracy_for_half_freq_words)

