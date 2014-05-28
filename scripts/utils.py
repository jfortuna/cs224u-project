import sys
import os
import liwc
from nltk import tokenize
import csv
import codecs
import cStringIO

def get_liwc_counts_from_utterance(utterance):
    tokens = tokenize_utterance(utterance)
    num_articles, num_aux_verbs, num_conjunctions, num_adverbs, num_ipronouns, num_ppronouns, num_prepositions, num_quantifiers = [0 for x in range(8)] 
    #initializing 8 different variables all to zero
    for token in tokens:
        if token in liwc.articles:
            num_articles += 1
        if token in liwc.aux_verbs:
            num_aux_verbs += 1
        if token in liwc.conjunctions:
            num_conjunctions += 1
        if token in liwc.adverbs:
            num_adverbs += 1
        if token in liwc.ipronouns:
            num_ipronouns += 1
        if token in liwc.ppronouns:
            num_ppronouns += 1
        if token in liwc.prepositions:
            num_prepositions += 1
        if token in liwc.quantifiers:
            num_quantifiers += 1
    return (num_articles, num_aux_verbs, num_conjunctions, num_adverbs, num_ipronouns, num_ppronouns, num_prepositions, num_quantifiers)

def tokenize_utterance(utterance):
    token_list = []
    sent_tokens = tokenize.sent_tokenize(utterance)
    for sent_token in sent_tokens:
        words = tokenize.word_tokenize(sent_token)
        token_list.append(words)
    return [item for sublist in token_list for item in sublist]



class UTF8Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode("utf-8")

class UnicodeReader:
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)

    def next(self):
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]

    def __iter__(self):
        return self

class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)
