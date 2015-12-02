# coding=utf-8
import codecs
import json
import random
import re
from os.path import join


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
        self.frequency_after_word = None
        self.frequency_after_pair = None
        self.load_corpus(corpus_name)

    def load_corpus(self, corpus_name):
        with codecs.open(join("corpus", corpus_name + ".json"), encoding='utf-8') as f:
            raw_json = f.read()
            corpus = json.loads(raw_json)

            self.starters = WordPicker.convert(corpus['starters'])
            self.frequency_after_word = corpus['frequency_after_word']
            self.frequency_after_pair = corpus['frequency_after_pair']

    def generate(self, words_count):
        i, count = 0, 0
        paragraphs = []
        sentences = []
        while count < words_count:
            print "\tSentence #" + str(i)
            new_sentence, sentence_words_count = self.generate_sentence()
            i += 1
            count += sentence_words_count
            sentences.append(new_sentence)
            if len(sentences) == 12:
                new_paragraph = " ".join(sentences)
                paragraphs.append(new_paragraph)
                sentences = []
        text = "\n".join(paragraphs)
        return self.post_processing(text)

    def generate_sentence(self):
        words = WordPicker.pick(self.starters).split()
        new_word = self.generate_second_word(words)
        if new_word is not None:
            words.append(new_word)

            while words[-1] != ".":
                new_word = self.generate_word(words)
                if new_word is not None and new_word != words[-1] \
                        and new_word != words[-2]:
                    words.append(new_word)
                else:
                    break
        words[0] = words[0].title()
        return " ".join(words), len(words)

    def generate_second_word(self, prev_words):
        prev_phrase = prev_words[-1]
        if prev_phrase in self.frequency_after_word:
            variants = self.frequency_after_word[prev_phrase]
            return WordPicker.pick_raw(variants)
        else:
            return None

    def generate_word(self, prev_words):
        prev_phrase = prev_words[-2] + u" " + prev_words[-1]
        if prev_phrase in self.frequency_after_pair:
            variants = self.frequency_after_pair[prev_phrase]
            return WordPicker.pick_raw(variants)
        else:
            return None

    def post_processing(self, text):
        text = re.sub(u'\s*([\.,])', r'\1', text)
        return re.sub(u',\.', u'.', text)

if __name__ == "__main__":
    author = "ruwiki"
    paragraph_len = 5

    print "Load corpus..."
    korchevatel = Korchevatel(author)
    print "Generate text..."
    text = korchevatel.generate(10000)
    print "Write file..."
    with open(author + ".txt", "wb") as f:
        f.write(text.encode('utf8'))
    print "Done!"
