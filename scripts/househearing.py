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


def pair_rank(raw_vectors, year_list):
    pair_data = []
    pair_target = []
    for hearing in raw_vectors:
        combos  = combinations(hearing.keys(), 2)
        for combo in combos:
            person1 = combo[0]
            person2 = combo[1]
            new_instance = hearing[person1] + hearing[person2]
            pair_data.append(new_instance)
            rel_rank = rank_lookup(person1, person2, year)
            if rel_rank!= 0: pair_target.append(rel_rank)


# def rank_lookup(x,y, year):



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
house_utterances, congress_year = readdata.read_house_hearing('../../data/small_house/')

print congress_year

# all_vectors = build_vectors()
# a = pair_rank(all_vectors)

# all_rank = read_rank_data()
# print all_rank['2011']['Bob Latta']
# print all_rank['2011']
