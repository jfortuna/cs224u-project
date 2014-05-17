from sklearn.feature_extraction.text import CountVectorizer
from sklearn import svm

import sys
import os
import readdata
import utils
import numpy

#TODO finish the bag of words stuff, 
#see http://scikit-learn.org/stable/modules/feature_extraction.html#the-bag-of-words-representation 
#and http://scikit-learn.org/stable/auto_examples/document_classification_20newsgroups.html for more info
def bag_of_words():
    vectorizer = CountVectorizer()

#TODO
def stylistic_features():
    # for a_speaker_pair in speaker_pairs:
    	# thisPair_sum = stylistic_features_helper(speaker_pair)
    pass
#TODO
#Do Macro-Averaging C(b, A)
def coordination_features():
    pass


def speaker_pair_sum_vectors(speaker_pair):
	b_a_sum= {}

	b_speaker = speaker_pair[1]
	a_target = speaker_pair[0]

	b_a_sum[b_speaker] = (0,0,0,0,0,0,0,0)
	b_a_sum[a_target] = (0,0,0,0,0,0,0,0)

	conversation = speaker_pairs[speaker_pair]
	for exchange in conversation:
		b_utterance = all_utterances[exchange[1]]['utterance']
		a_utterance = all_utterances[exchange[0]]['utterance']

		b_utter_vec = utils.get_liwc_counts_from_utterance(b_utterance)
		a_utter_vec = utils.get_liwc_counts_from_utterance(a_utterance)

		b_a_sum[b_speaker] = tuple(numpy.array(b_a_sum[b_speaker]) + numpy.array(b_utter_vec)) 
		b_a_sum[a_target] = tuple(numpy.array(b_a_sum[a_target]) + numpy.array(a_utter_vec)) 

	return b_a_sum

def speaker_pair_coordination(speaker_pair):

	b_speaker = speaker_pair[1]
	a_target = speaker_pair[0]

	b_coord_a_counts = (0,0,0,0,0,0,0,0)

	conversation = speaker_pairs[speaker_pair]
	for exchange in conversation:
		curr_counts = count_coordination(exchange)

		b_coord_a_counts = tuple(numpy.array(b_coord_a_counts) + numpy.array(curr_counts))

	return b_coord_a_counts


def count_coordination(utterance_pair):
	b_utterance = all_utterances[utterance_pair[1]]['utterance']
	a_utterance = all_utterances[utterance_pair[0]]['utterance']

	b_utter_vec = utils.get_liwc_counts_from_utterance(b_utterance)
	a_utter_vec = utils.get_liwc_counts_from_utterance(a_utterance)

	coordination_counts = [0,0,0,0,0,0,0,0]
	for marker_id in range(1,8):
		
		if (a_utter_vec[marker_id] > 0) and (b_utter_vec[marker_id] > 0):
			coordination_counts[marker_id] = coordination_counts[marker_id] + 1;

	return coordination_counts

#testing get_liwc_counts_from_utterances
all_utterances, speaker_pairs = readdata.read_supreme_court()
# test = all_utterances[2]['utterance']
# print utils.get_liwc_counts_from_utterance(test)

print speaker_pairs[('JUSTICE KENNEDY', 'MR. MCNULTY')]

print utils.get_liwc_counts_from_utterance(all_utterances[42325]['utterance'])
print utils.get_liwc_counts_from_utterance(all_utterances[42326]['utterance'])
print utils.get_liwc_counts_from_utterance(all_utterances[42329]['utterance'])
print utils.get_liwc_counts_from_utterance(all_utterances[42330]['utterance'])
print utils.get_liwc_counts_from_utterance(all_utterances[42334]['utterance'])
print utils.get_liwc_counts_from_utterance(all_utterances[42335]['utterance'])
print utils.get_liwc_counts_from_utterance(all_utterances[42343]['utterance'])
print utils.get_liwc_counts_from_utterance(all_utterances[42344]['utterance'])

print ""
print speaker_pair_coordination(('JUSTICE KENNEDY', 'MR. MCNULTY'))
# print utils.get_liwc_counts_from_utterance(test)
