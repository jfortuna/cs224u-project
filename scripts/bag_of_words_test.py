from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.linear_model import LogisticRegression
from sklearn.grid_search import GridSearchCV
from sklearn.cross_validation import train_test_split, cross_val_score
from sklearn import metrics

import sys
import os
import readdata
import utils
import numpy as np

#
# using 0 to represent first person is of higher status than second person
# using 1 to represent first person is of lower status than second person
#
high = 0
low = 1
error = 2

def get_replies(conversations, speaker):
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
    mod = LogisticRegression(fit_intercept=True, intercept_scaling=1)
    parameters = {'C':[x / 10.0 for x in range(1,20)], 'penalty':['l1','l2']}
    dataset = build_dataset(max_features=5000, min_df=1)
    X = dataset['features']
    y = dataset['labels']
    dev_feats, experiment_feats, dev_labels, experiment_labels = train_test_split(X, y, test_size=0.5)
    selector = SelectKBest(chi2, k=5000)
    dev_feats = selector.fit_transform(dev_feats, dev_labels)
    clf = GridSearchCV(mod, parameters, cv=10)
    clf.fit(dev_feats, dev_labels)
    params = clf.best_params_
    experiment_feats = experiment_feats[ : , selector.get_support(indices=True)]
    mod = LogisticRegression(fit_intercept=True, intercept_scaling=1, C=params['C'], penalty=params['penalty'])
    scores = cross_val_score(mod, experiment_feats, experiment_labels, cv=10, scoring='accuracy')
    print 'Best model', mod
    print 'Accuracy scores', scores
    print 'Mean accuracy score', np.mean(scores)

def build_dataset(max_features=5000, min_df=1):
    v = CountVectorizer(ngram_range=(1,1), min_df=min_df)
    data_target = []
    data = []
    for pair, conversations in speaker_pairs.iteritems():
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
            data_target.append(label)
            data.append(conversation_x_y)
    X = v.fit_transform(data)
    return {'features': X, 'labels': np.array(data_target), 'featurenames': v.get_feature_names()}


all_utterances, speaker_pairs = readdata.read_supreme_court()
bag_of_words()
