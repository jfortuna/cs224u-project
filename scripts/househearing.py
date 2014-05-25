import readdata
import utils
from operator import add
from itertools import combinations


def build_vectors():
    all_vectors = []
    for hearing in house_utterances:
        hearing_map = {}
        for speaker, list_of_utterances in hearing.iteritems():
            all_vectors[][speaker] = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
            for utterance in list_of_utterances:
                # print utterance
                new_vector = utils.get_liwc_counts_from_utterance(utterance)
                # print new_vector
                all_vectors[speaker] = map(add,  all_vectors[speaker], list(new_vector))
    return all_vectors


def pair_rank(raw_vectors):
    pair_data = []
    pair_target = []
    for hearing in raw_vectors:
        combos  = combinations(raw_vectors.keys(), 2)
    for combo in combos:
        new_instance = raw_vectors[]


house_utterances = readdata.read_house_hearing('../../data/small_house/')

all_vectors = build_vectors()
a = pair_rank(all_vectors)