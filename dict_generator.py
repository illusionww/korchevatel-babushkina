# coding=utf-8
import codecs
import json
import re
from collections import defaultdict
from os import listdir
from os.path import isfile, join


class Corpus(object):
    def __init__(self):
        self.starters = defaultdict(int)
        self.frequency_after_word = defaultdict(lambda: defaultdict(int))
        self.frequency_after_pair = defaultdict(lambda: defaultdict(int))

    def process(self, folder):
        books = [join(folder, f) for f in listdir(unicode(folder)) if
                 isfile(join(folder, f))]
        count = len(books)
        for i in xrange(count):
            print "Process file #" + str(i + 1) + "/" + str(count)
            self.process_book(books[i])

    def process_book(self, book):
        with codecs.open(book, encoding='utf-8') as f:
            text = self.clean_text(f.read())
        paragraphs = text.split('\n')
        for paragraph in paragraphs:
            sentences = paragraph.split('|')
            for sentence in sentences:
                sentence = sentence.strip()
                if len(sentence) > 1:
                    sentence = sentence[0].lower() + sentence[1:]
                    self.process_sentence(sentence)

    def process_sentence(self, sentence):
        words = [word for word in sentence.split()
                 if word not in [',', '-', '\'']]
        if len(words) > 2:
            self.starters[words[0]] += 1
            for prev, word in [(words[i - 1], words[i])
                               for i in xrange(1, len(words))]:
                self.frequency_after_word[prev][word] += 1
            for pair, word in [(words[i - 2] + " " + words[i - 1], words[i])
                               for i in xrange(2, len(words))]:
                self.frequency_after_pair[pair][word] += 1
            self.frequency_after_pair[words[-2] + " " + words[-1]]['.'] += 1

    def clean_text(self, text):
        # replace endings, quotes, dashes, ё
        text = text.replace('\r\n', '\n').replace('\r', '\n') \
            .replace('\"', '.').replace('--', ' ').replace(u'ё', u'е') \
            .replace(u'\u00AB', '.').replace(u'\u00BB', '.')
        # delete {{ }} wiki metainformation
        text = re.sub(u'\{\{[^\\r]*?\}\}', u' ', text)
        # delete < > tags
        text = re.sub(u'<[^\\r]*?>', u' ', text)
        # replace [[ ]] wiki links into link text, delete external links [ ]
        text = re.sub(u'\[\[([^\|]+?)\]\]', r'\1', text)
        text = re.sub(u'\[\[.+?\|(.+?)\]\]', r'\1', text)
        text = re.sub(u'\[.+?\]', u' ', text)
        # delete all symbols inside ( )
        text = re.sub(u'\(.+?\)', u' ', text)
        # delete all symbols except \w . , - ' and \n
        text = re.sub(u'[^\wа-яА-Я,\-\.\n\' ]', u' ', text)
        text = re.sub(u'\s[,\-]+\s', u' ', text)
        # fix commas
        text = re.sub(u'\s*([,\.])\s*', r'\1 ', text)
        text = re.sub(u'\s?\'\s?', u' ', text)
        # split sentences
        text = re.sub(u'\s*\.\s*([A-ZА-Я])', r'|\1', text)
        text = re.sub(u'\s*\.\s*\\n', u'\n', text)
        # delete dots
        return text.replace(u'.', ' ')


if __name__ == "__main__":
    author = "default"

    print "Process files..."
    corpus = Corpus()
    corpus.process(join("corpus", author))
    print "Create json..."
    json_data = json.dumps({
        'starters': corpus.starters,
        'frequency_after_word': corpus.frequency_after_word,
        'frequency_after_pair': corpus.frequency_after_pair
    }, ensure_ascii=False).encode('utf8')
    print "Write json..."
    with open(join("corpus", author + ".json"), "wb") as f:
        f.write(json_data)
    print "Done!"
