import readdata
import utils
from operator import add
from itertools import combinations


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
    for hearing in raw_vectors:
        combos  = combinations(hearing.keys(), 2)
        for combo in combos:
            person1 = combo[0]
            person2 = combo[1]
            new_instance = hearing[person1] + hearing[person2]
            pair_data.append(new_instance)
            rel_rank = rank_lookup(person1, person2, year)
            if rel_rank!= 0: pair_target.append(rel_rank)


def rank_lookup(x,y, year):
    


house_utterances = readdata.read_house_hearing('../../data/small_house/')

all_vectors = build_vectors()
a = pair_rank(all_vectors)