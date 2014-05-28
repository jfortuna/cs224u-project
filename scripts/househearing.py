from __future__ import division
import readdata
import utils
from itertools import combinations
import csv
import collections
import os
import codecs
from sklearn import cross_validation
from sklearn import metrics
from sklearn import svm
import numpy as np
import sys


######
# articles
# aux_verbs
# conjunctions
# adverbs
# ipronouns
# ppronouns
# prepositions
# quantifiers
# singppronouns
# pluralppronouns
####
sys.stdout = codecs.getwriter('utf-8')(sys.__stdout__)

def get_avg_utterance_length(num_utterances, combined_utterances):
    return [len(combined_utterances.split())/num_utterances]

def get_liwc_features(combined_utterances):
    return list(utils.get_liwc_counts_from_utterance(combined_utterances))

def get_sum_utterance_length(combined_utterances):
    return [len(combined_utterances.split())]

def build_vectors():
    all_vectors = []
    for index, hearing in enumerate(house_utterances):
        print 'Building vectors for hearing', index
        hearing_map = {}
        for speaker, utterances in hearing.iteritems():
            combined_utterances = ' '.join(utterances)
            hearing_map[speaker] = get_avg_utterance_length(len(utterances), combined_utterances) + \
                                get_sum_utterance_length(combined_utterances) + \
                                utils.get_liwc_features_of_interest(combined_utterances, ['singppronouns', 'pluralppronouns'])
            #get_avg_utterance_length + get_liwc_features + get_sum_utterance_length
        all_vectors.append(hearing_map)
    return all_vectors

def concat_vectors(person1_vector, person2_vector):
    return person1_vector + person2_vector

def diff_vectors(person1_vector, person2_vector):
    return [x - y for x,y in zip(person1_vector, person2_vector)]

def pair_rank(raw_vectors):
    pair_data = []
    pair_target = []
    for index, hearing in enumerate(raw_vectors):
        print 'Calculating ranks for hearing', index
        combos  = combinations(hearing.keys(), 2)
        for combo in combos:
            year = congress_year[index]
            person1 = combo[0]
            person2 = combo[1]
            new_instance = concat_vectors(hearing[person1], hearing[person2])
            year = congress_year[index]
            rel_rank = rank_lookup(person1, person2, year)
            if rel_rank!= -1 and rel_rank != None:
                pair_target.append(rel_rank)
                pair_data.append(new_instance)
    # print pair_data
    # print pair_target
    return (pair_data, pair_target)


def rank_lookup(x,y, year):
    no_vote_members = set(['Donna Christensen', 'Gregorio Sablan', 'Pedro Pierluisi', 'Eleanor Norton', 'Eni Faleomavaega', 'Madeleine Bordallo'])
    try:
        all_rank[year][x]
    except KeyError:
        if not x in no_vote_members:
            keyerrors.add(x)
        return -1;
    try:
        all_rank[year][y]
    except KeyError:
        if not y in no_vote_members:
            keyerrors.add(y)
        return -1;

    if abs(all_rank[year][x] - all_rank[year][y]) > 20:
        if (all_rank[year][x] > all_rank[year][y]): return 1
        if (all_rank[year][x] < all_rank[year][y]): return 0
        else: return -1
    else: return -1

def read_rank_data(dirname = 'rank/'):
    all_rank = collections.defaultdict(lambda:{})
    base_path = dirname
    for filename in os.listdir(base_path):
        year = filename[:4]
        with open(base_path + filename) as csvfile:
            reader = utils.UnicodeReader(csvfile, delimiter = ",")
            for row in reader:
                all_rank[year][row[1]] = row[0]
    print "Rank data read"
    return all_rank

def svm_cv(data, data_target):
	X_train, X_test, y_train, y_test = cross_validation.train_test_split(data, data_target)
	print "Training..."
	clf = svm.LinearSVC()
	clf.fit(X_train, y_train)
	print "Testing..."
	pred = clf.predict(X_test)
	accuracy_score = metrics.accuracy_score(y_test, pred)
	classification_report = metrics.classification_report(y_test, pred)
	print accuracy_score
	print classification_report
	np.set_printoptions(threshold='nan')
	#print y_test
	#print pred


all_rank = read_rank_data()
# house_utterances, congress_year = readdata.read_house_hearing(dirname='../../data/small_house/')
house_utterances, congress_year = readdata.read_house_hearing()
all_vectors = build_vectors()

# print all_rank
keyerrors = set([])   
data, target = pair_rank(all_vectors)
# print keyerrors
svm_cv(data, target)
