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

#see http://scikit-learn.org/stable/modules/feature_extraction.html#the-bag-of-words-representation 
#and http://scikit-learn.org/stable/auto_examples/document_classification_20newsgroups.html for more info
def bag_of_words():
    all_utterances, speaker_pairs = readdata.read_supreme_court()
    data_target = []
    data = []
    pairs = []
    for pair, conversations in speaker_pairs.iteritems():
        conversation_x_y = ""
        label = error
        for conversation in conversations:
            x = all_utterances[conversation[0]]
            y = all_utterances[conversation[1]]
            utterance_x = utils.tokenize_utterance(x['utterance'])
            utterance_y = utils.tokenize_utterance(y['utterance'])
            if x['is_justice'] and not y['is_justice']:
                label = high
            elif not x['is_justice'] and y['is_justice']:
                label = low
            if abs(len(utterance_x) - len(utterance_y)) >= 20:
                label = error
            conversation_x_y += " ".join(utterance_x) + " "
            conversation_x_y += " ".join(utterance_y) + " "
        if label != error:
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
    accuracy_score = metrics.zero_one_score(y_test, pred)
    classification_report = metrics.classification_report(y_test, pred)
    print accuracy_score
    print classification_report
    numpy.set_printoptions(threshold='nan')
    print y_test
    print pred

bag_of_words()
