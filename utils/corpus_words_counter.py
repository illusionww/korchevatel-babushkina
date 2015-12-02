# coding=utf-8
import codecs
import re
from os import listdir
from os.path import isfile, join


class Counter(object):
    def __init__(self):
        self.count = 0

    def process(self, folder):
        books = [join(folder, f) for f in listdir(unicode(folder)) if
                 isfile(join(folder, f))]
        for i in xrange(len(books)):
            self.process_book(books[i])

    def process_book(self, book):
        with codecs.open(book, encoding='utf-8') as f:
            text = self.clean_text(f.read())
        self.count += len(text.split())

    def clean_text(self, text):
        text = re.sub(u' \-+ ', u' ', text)
        return re.sub(u'[^\wа-яА-Я\- ]', u' ', text)


if __name__ == "__main__":
    author = "default"

    corpus = Counter()
    corpus.process(join("../corpus", author))
    print corpus.count
