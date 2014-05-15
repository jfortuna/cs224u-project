from sklearn.feature_extraction.text import CountVectorizer
from sklearn import svm
from nltk import tokenize

import sys
import os
import readdata
import liwc

def bag_of_words():
    all_utterances, speaker_pairs = readdata.read_supreme_court()
    test = all_utterances[2]['utterance']
    print test
    sent_tokens = tokenize.sent_tokenize(test)
    for sent_token in sent_tokens:
        words = tokenize.word_tokenize(sent_token)
        print words
        if liwc.articles & set(words):
            print "articles"

def stylistic_features():
    pass
    #TODO

def coordination_features():
    pass
    #TODO

bag_of_words()
