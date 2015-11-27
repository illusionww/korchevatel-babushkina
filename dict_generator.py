# coding=UTF-8
import codecs
import json
import re
from collections import defaultdict
from os import listdir
from os.path import isfile, join


class Corpus(object):
    def __init__(self, folder):
        self.starters = defaultdict(int)
        self.frequency_after_word = defaultdict(lambda: defaultdict(int))
        self.frequency_after_pair = defaultdict(lambda: defaultdict(int))

        books = [join(folder, f) for f in listdir(folder) if
                 isfile(join(folder, f))]
        for book in books:
            print "Process book " + book
            self.process_book(book)

    def process_book(self, book):
        with codecs.open(book, encoding='utf-8') as f:
            text = self.clean_text(f.read())
        paragraphs = text.split('\n')
        for paragraph in paragraphs:
            sentences = paragraph.split('.')
            for sentence in sentences:
                sentence = sentence.strip()
                if len(sentence) > 1:
                    sentence = sentence[0].lower() + sentence[1:]
                    self.process_sentence(sentence)

    def process_sentence(self, sentence):
        words = sentence.split()
        if len(words) > 2:
            self.starters[words[0] + " " + words[1]] += 1
            for pair, word in [(words[i - 1], words[i]) for i in
                               xrange(1, len(words))]:
                self.frequency_after_word[pair][word] += 1
            for pair, word in [(words[i - 2] + " " + words[i - 1], words[i])
                               for i in xrange(2, len(words))]:
                self.frequency_after_pair[pair][word] += 1

    def clean_text(self, text):
        text = text.replace('\r\n', '\n').replace('\r', '\n') \
            .replace('--', ' ').replace('\"', '.')\
            .replace(u'\u00AB', '.').replace(u'\u00BB', '.')
        return re.sub(u'[^\wа-яА-Я,\-\.\n ]', ' ', text)

    def get_statistics(self, sentence):
        pass


if __name__ == "__main__":
    author = "dontsova"

    print "Generate dictionary..."
    corpus = Corpus(join("corpus", author))
    print "Create json..."
    json_data = json.dumps({
        'starters': corpus.starters,
        'frequency_after_pair': corpus.frequency_after_pair
    }, ensure_ascii=False).encode('utf8')
    print "Write json..."
    with open(join("corpus", author + ".json"), "wb",) as f:
        f.write(json_data)
    print "Done!"
