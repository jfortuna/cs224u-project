import readdata
import utils
from operator import add
from itertools import combinations
import csv
import collections
import os
import codecs
import cStringIO

def build_vectors():
    all_vectors = []
    for hearing in house_utterances:
        hearing_map = {}
        for speaker, list_of_utterances in hearing.iteritems():
            hearing_map[speaker] = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
            for utterance in list_of_utterances:
                # print utterance
                new_vector = utils.get_liwc_counts_from_utterance(utterance)
                # print new_vector
                hearing_map[speaker] = map(add,  hearing_map[speaker], list(new_vector))
        all_vectors.append(hearing_map)
    return all_vectors


def pair_rank(raw_vectors):
    pair_data = []
    pair_target = []
    for index, hearing in enumerate(raw_vectors):
        combos  = combinations(hearing.keys(), 2)
        for combo in combos:
            person1 = str(combo[0])
            person2 = str(combo[1])
            print person1, person2
            new_instance = hearing[person1] + hearing[person2]
            year = congress_year[index]
            print year
            rel_rank = rank_lookup(person1, person2, year)
            if rel_rank!= -1: 
                pair_target = (rel_rank)
                pair_data.append(new_instance)

    return (pair_data, pair_target)


def rank_lookup(x,y, year):
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

class UTF8Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

<<<<<<< HEAD
=======
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


>>>>>>> c25a2b4f20e6d3d4945774f1a0384274ce41d2ee
all_rank = read_rank_data()
house_utterances, congress_year = readdata.read_house_hearing('../../data/small_house/')
all_vectors = build_vectors()

# print all_rank
print pair_rank(all_vectors)

# all_vectors = build_vectors()
# a = pair_rank(all_vectors)

# all_rank = read_rank_data()
# print all_rank['2011']['Bob Latta']
# print all_rank['2011']
