import json
from collections import defaultdict
from os import listdir
from os.path import isfile, join
import codecs


class Corpus:
    def __init__(self, folder):
        self.starters = defaultdict(int)
        self.enders = defaultdict(int)
        self.frequency_after_word = defaultdict(lambda : defaultdict(int))
        self.frequency_after_pair = defaultdict(lambda : defaultdict(int))

        books = [join(folder, f) for f in listdir(folder) if isfile(join(folder, f))]
        for book in books:
            print "Process book " + book
            self.process_book(book)

    def process_book(self, book):
        with codecs.open(book) as f:
            text = self.clean_text(f.read())
            text = text.decode('unicode_escape').encode('ascii','ignore')
        sentences = text.split('.')
        for sentence in sentences:
            self.process_sentence(sentence)

    def process_sentence(self, sentence):
        words = sentence.split()
        if len(words) > 0:
            self.starters[words[0]] += 1
            self.enders[words[-1]] += 1
            for pair, word in [(words[i-1], words[i]) for i in xrange(1, len(words))]:
                self.frequency_after_word[pair][word] += 1
            for pair, word in [(words[i-2] + " " + words[i-1], words[i]) for i in xrange(2, len(words))]:
                self.frequency_after_pair[pair][word] += 1

    def clean_text(self, text):
        return text.lower().replace('\r\n', '\n').replace('\r', '\n') \
            .replace('-\n', '').replace('--', '').replace(' -', '')\
            .replace('- ', '').replace(' -', '').replace('\n', ' ')\
            .translate(None, ',:;"!?#%^&*@_()[]{}+\\=<>/\'')

    def get_statistics(self, text):
        pass

if __name__ == "__main__":
    print "Generate dictionary..."
    corpus = Corpus("corpus/asimov")
    print "Create json..."
    json_data = json.dumps({
        'starters': corpus.starters,
        'enders': corpus.enders,
        'frequency_after_pair': corpus.frequency_after_pair
    }, sort_keys=True, indent=4, separators=(',', ': '))
    print "Write json..."
    with open("asimov.json", "w") as f:
        f.write(json_data)
    print "Done!"