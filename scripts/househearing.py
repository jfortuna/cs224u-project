import readdata
import utils
from itertools import combinations
import csv
import collections
import os
import codecs
import cStringIO
from sklearn import cross_validation
from sklearn import metrics
from sklearn import svm
import numpy as np
import sys


def build_vectors():
    print len(house_utterances)
    all_vectors = []
    for index, hearing in enumerate(house_utterances):
        # print 'Building vectors for hearing', index
        hearing_map = {}
        for speaker, utterances in hearing.iteritems():
            combined_utterances = ' '.join(utterances)
            hearing_map[speaker] = list(utils.get_liwc_counts_from_utterance(combined_utterances))
        all_vectors.append(hearing_map)
    return all_vectors


def pair_rank(raw_vectors):
    pair_data = []
    pair_target = []
    for index, hearing in enumerate(raw_vectors):
        # print 'Calculating ranks for hearing', index
        combos  = combinations(hearing.keys(), 2)
        for combo in combos:
            year = congress_year[index]
            # print year
            person1 = combo[0]
            # print combo
            person2 = combo[1]
            # print person1, person2

            new_instance = hearing[person1] + hearing[person2]
            # print index
            year = congress_year[index]
            # print year
            rel_rank = rank_lookup(person1, person2, year)
            if rel_rank!= -1 and rel_rank != None:
                pair_target.append(rel_rank)
                pair_data.append(new_instance)

    # print pair_data
    # print pair_target
    return (pair_data, pair_target)


def rank_lookup(x,y, year):
    no_vote_members = set(['Donna Christensen', 'Gregorio Sablan', 'Pedro Pierluisi', 
                        'Eleanor Norton', 'Eni Faleomavaega', 'Madeleine Bordallo'])
    if x.encode('utf-8').find('Ra\xc3\xbal Grijalva') > -1: x ='Raul Grijalva'
    if y.encode('utf-8').find('Ra\xc3\xbal Grijalva') > -1: y ='Raul Grijalva'    
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
    if (all_rank[year][x] > all_rank[year][y]): return 1
    if (all_rank[year][x] < all_rank[year][y]): return 0
    else: -1

def read_rank_data(dirname = 'rank/'):
    all_rank = collections.defaultdict(lambda:{})
    base_path = dirname
    for filename in os.listdir(base_path):
        year = filename[:4]
        with open(base_path + filename) as csvfile:
            reader = UnicodeReader(csvfile, delimiter = ",")
            for row in reader:
                all_rank[year][row[1]] = row[0]
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

all_rank = read_rank_data()
house_utterances, congress_year = readdata.read_house_hearing()
all_vectors = build_vectors()

# print all_rank
keyerrors = set([])   
data, target = pair_rank(all_vectors)
print keyerrors
# svm_cv(data, target)

# all_vectors = build_vectors()
# a = pair_rank(all_vectors)

# all_rank = read_rank_data()
# print all_rank['2011']['Bob Latta']
# print all_rank['2011']
