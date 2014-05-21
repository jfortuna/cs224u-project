from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
from sklearn import cross_validation
from sklearn import metrics

import sys
import os
import readdata
import utils
import numpy

#
# using 0 to represent first person is of higher status than second person
# using 1 to represent first person is of lower status than second person
#
high = 0
low = 1
error = 2

def get_replies(conversations):
    replies = []
    for conversation in conversations:
        u_1 = all_utterances[conversation[0]]['utterance']
        u_2 = all_utterances[conversation[1]]['utterance']
        if abs(len(u_1.split()) - len(u_2.split())) < 20:
            replies.append(u_2)
    return " ".join(replies)

#see http://scikit-learn.org/stable/modules/feature_extraction.html#the-bag-of-words-representation 
#and http://scikit-learn.org/stable/auto_examples/document_classification_20newsgroups.html for more info
def bag_of_words():
    data_target = []
    data = []
    pairs = []
    already_checked_pairs = set()
    #get pair and partner (by flipping pair), append to set of running ones I've checked already
    for pair, conversations in speaker_pairs.iteritems():
        if pair not in already_checked_pairs:
            already_checked_pairs.add(pair)
            x_is_high = all_utterances[conversations[0][0]]['is_justice']
            y_is_high = all_utterances[conversations[0][1]]['is_justice']
            if x_is_high and not y_is_high:
                label = high
            elif not x_is_high and y_is_high:
                label = low
            else:
                label = error
            if label != error:
                conversation_x_y = get_replies(conversations)
                pairs.append(pair)
                data_target.append(label)
                data.append(conversation_x_y)
    #print data_target
    #print data
    data_train, data_test, y_train, y_test = cross_validation.train_test_split(data, data_target)
    print "Extracting features"
    vectorizer = TfidfVectorizer(norm = 'l2')
    X_train = vectorizer.fit_transform(data_train)
    print len(vectorizer.get_feature_names())
    X_test = vectorizer.transform(data_test)
    print "Training"
    clf = svm.LinearSVC()
    clf.fit(X_train, y_train)
    print "Testing"
    pred = clf.predict(X_test)
    accuracy_score = metrics.accuracy_score(y_test, pred)
    classification_report = metrics.classification_report(y_test, pred)
    print accuracy_score
    print classification_report
    numpy.set_printoptions(threshold='nan')
    print y_test
    print pred

all_utterances, speaker_pairs = readdata.read_supreme_court()
bag_of_words()
