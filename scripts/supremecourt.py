from sklearn.feature_extraction.text import CountVectorizer
from sklearn import svm
from nltk import tokenize

import sys
import os
import readdata
import utils

def bag_of_words():
    pass
    #TODO

def stylistic_features():
    pass
    #TODO

def coordination_features():
    pass
    #TODO


#testing get_liwc_counts_from_utterances
all_utterances, speaker_pairs = readdata.read_supreme_court()
test = all_utterances[2]['utterance']
print test
print utils.get_liwc_counts_from_utterance(test)
