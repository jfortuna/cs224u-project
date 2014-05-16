from sklearn.feature_extraction.text import CountVectorizer
from sklearn import svm

import sys
import os
import readdata
import utils

#TODO finish the bag of words stuff, see http://scikit-learn.org/stable/modules/feature_extraction.html#the-bag-of-words-representation and http://scikit-learn.org/stable/auto_examples/document_classification_20newsgroups.html for more info
def bag_of_words():
    vectorizer = CountVectorizer()

#TODO
def stylistic_features():
    pass

#TODO
def coordination_features():
    pass


#testing get_liwc_counts_from_utterances
all_utterances, speaker_pairs = readdata.read_supreme_court()
test = all_utterances[2]['utterance']
print test
print utils.get_liwc_counts_from_utterance(test)
