import codecs
import json
import random
from os.path import join

sentence_len = 10
paragraph_len = 5


class WordPicker(object):
    @staticmethod
    def convert(raw_data):
        variants = []
        prev_count = 0
        for key, value in raw_data.items():
            variants.append((prev_count, key))
            prev_count += value
        return variants, prev_count

    @staticmethod
    def pick(converted):
        data, max_value = converted
        value = random.randint(0, max_value)

        size = len(data)
        index = 0
        while index < size - 1 and data[index][0] <= value:
            index += 1
        return data[index][1]

    @staticmethod
    def pick_raw(raw_data):
        converted = WordPicker.convert(raw_data)
        return WordPicker.pick(converted)


class Korchevatel(object):
    def __init__(self, corpus_name):
        self.starters = None
        self.frequency_after_pair = None
        self.load_corpus(corpus_name)

    def load_corpus(self, corpus_name):
        with codecs.open(join("corpus", corpus_name + ".json"), encoding='utf-8') as f:
            raw_json = f.read()
            corpus = json.loads(raw_json)

            self.starters = WordPicker.convert(corpus['starters'])
            self.frequency_after_pair = corpus['frequency_after_pair']

    def generate(self, words_count):
        count_sentences = words_count // sentence_len
        count_paragraphs = count_sentences // paragraph_len

        paragraphs = []
        for i in xrange(count_paragraphs):
            new_paragraph = self.generate_paragraph()
            paragraphs.append(new_paragraph)
        return "\n".join(paragraphs)

    def generate_paragraph(self):
        sentences = []
        for i in xrange(paragraph_len):
            new_sentence = self.generate_sentence()
            sentences.append(new_sentence)
        return " ".join(sentences)

    def generate_sentence(self):
        words = WordPicker.pick(self.starters).split()
        current_len = 2
        while current_len < sentence_len or self.get_prev_frequency(words) > 40:
            new_word = self.generate_word(words)
            if new_word is not None:
                words.append(new_word)
            else:
                break
        words[0] = words[0].title()
        return " ".join(words) + "."

    def generate_word(self, prev_words):
        prev_phrase = prev_words[-2] + u" " + prev_words[-1]
        if prev_phrase in self.frequency_after_pair:
            variants = self.frequency_after_pair[prev_phrase]
            return WordPicker.pick_raw(variants)
        else:
            return None

    def get_prev_frequency(self, prev_words):
        prev_phrase = prev_words[-2] + u" " + prev_words[-1]
        if prev_phrase in self.frequency_after_pair:
            variants = self.frequency_after_pair[prev_phrase]
            return WordPicker.convert(variants)[1]
        else:
            return None

if __name__ == "__main__":
    author = "dontsova"

    korchevatel = Korchevatel(author)
    text = korchevatel.generate(1000)
    with open(author + ".txt", "wb") as f:
        f.write(text.encode('utf8'))
