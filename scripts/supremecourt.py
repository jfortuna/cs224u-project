from sklearn.feature_extraction.text import CountVectorizer
from sklearn import svm

import sys
import os
import readdata
import utils
import numpy
import supremecourt_utils

#
# using 1 to represent High Status Person
# using -1 to represent Low Status Person
#

#TODO finish the bag of words stuff, 
#see http://scikit-learn.org/stable/modules/feature_extraction.html#the-bag-of-words-representation 
#and http://scikit-learn.org/stable/auto_examples/document_classification_20newsgroups.html for more info
def bag_of_words():
    vectorizer = CountVectorizer()

#TODO
def stylistic_features(all_speaker_pairs):
	#includes average length of all 
	pass
#TODO

def coordination_features(all_speaker_pairs, all_utterances):
	#TODO Macro-Averaging C(b, A)
	print "Takes about ~2min to finish.....grab a cup of coffee"
	allscores = {}
	high = -1
	low = 1
	error = 0
	for pair, conversation in all_speaker_pairs.iteritems():
		# print str(pair) + ": " + str(conversation)
		# score = speaker_pair_coordination(pair, conversation)
		svm_vector = []
		label = error
		if (pair[0].find('JUSTICE') > -1 and pair[1].find('JUSTICE') == -1):
			label = high
		if (pair[0].find('CHIEF') > -1 and pair[1].find('CHIEF') == -1):
			label = high
		else:
			label = low
		svm_vector.append(label)
		svm_vector.append(supremecourt_utils.speaker_pair_coordination(pair, conversation))
		allscores[pair] = svm_vector
		# print allscores[pair]

	return allscores

def speaker_pair_coordination(speaker_pair, conversation):
	# print speaker_pair
	b_speaker = speaker_pair[1]
	a_target = speaker_pair[0]

	b_coord_a_counts = (0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0)
	b_exhibits_counts = (0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0)
	a_exhibits_counts = (0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0)

	for exchange in conversation:
		curr_coord = count_coordination(exchange)		
		b_coord_a_counts = tuple(numpy.array(b_coord_a_counts) + numpy.array(curr_coord))
		
		b_curr_exhibits = count_exhibits_feature(exchange, 1)
		a_curr_exhibits = count_exhibits_feature(exchange, 0)

		b_exhibits_counts = tuple(numpy.array(b_exhibits_counts) + numpy.array(b_curr_exhibits))
		a_exhibits_counts = tuple(numpy.array(a_exhibits_counts) + numpy.array(a_curr_exhibits))

	return calc_coordination(len(conversation), b_coord_a_counts, b_exhibits_counts, a_exhibits_counts)


def count_coordination(utterance_pair):
	b_utterance = all_utterances[utterance_pair[1]]['utterance']
	a_utterance = all_utterances[utterance_pair[0]]['utterance']

	b_utter_vec = utils.get_liwc_counts_from_utterance(b_utterance)
	a_utter_vec = utils.get_liwc_counts_from_utterance(a_utterance)

	coordination_counts = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
	for marker_id in range(0,8):
		
		if (a_utter_vec[marker_id] > 0) and (b_utter_vec[marker_id] > 0):
			coordination_counts[marker_id] = coordination_counts[marker_id] + 1.0;

	return coordination_counts

def count_exhibits_feature(utterance_pair, speaker):
	utterance = all_utterances[utterance_pair[speaker]]['utterance']
	utter_vec = utils.get_liwc_counts_from_utterance(utterance)

	exhibits_feature_counts = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
	for marker_id in range(0,8):
		
		if utter_vec[marker_id] > 0:
			exhibits_feature_counts[marker_id] = exhibits_feature_counts[marker_id] + 1.0;
	return exhibits_feature_counts


def calc_coordination(num_exchange, coordination_counts, b_exhibits_counts, a_exhibits_counts):
	# print coordination_counts
	# print b_exhibits_counts
	# print a_exhibits_counts

	coordination_prob = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
	for i in xrange(0, len(coordination_counts)):
		if coordination_counts[i] == 0.0:
			coordination_prob[i] = 0.0
		else:
			coordination_prob[i] = coordination_counts[i] / a_exhibits_counts[i];

	# coordination_prob = tuple(numpy.array(coordination_counts) / numpy.array(a_exhibits_counts));
	b_exhibits_prob = tuple(numpy.array(b_exhibits_counts) / num_exchange);

	coord_prob = tuple(numpy.array(coordination_prob) - numpy.array(b_exhibits_prob))
	# print coord_prob
	return coord_prob


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
#testing get_liwc_counts_from_utterances
all_utterances, speaker_pairs = readdata.read_supreme_court()
# test = all_utterances[2]['utterance']
# print utils.get_liwc_counts_from_utterance(test)

# for pair, conversation in speaker_pairs.iteritems():
# 	print speaker_pair_coordination(pair, conversation)
# print speaker_pairs[('JUSTICE KENNEDY', 'MR. MCNULTY')]
# print all_utterances[42325]['utterance']
# print utils.get_liwc_counts_from_utterance(all_utterances[42325]['utterance'])
# print utils.get_liwc_counts_from_utterance(all_utterances[42326]['utterance'])
# print utils.get_liwc_counts_from_utterance(all_utterances[42329]['utterance'])
# print utils.get_liwc_counts_from_utterance(all_utterances[42330]['utterance'])
# print utils.get_liwc_counts_from_utterance(all_utterances[42334]['utterance'])
# print utils.get_liwc_counts_from_utterance(all_utterances[42335]['utterance'])
# print utils.get_liwc_counts_from_utterance(all_utterances[42343]['utterance'])
# print utils.get_liwc_counts_from_utterance(all_utterances[42344]['utterance'])

# # print stylistic_features(speaker_pairs)
# print ('JUSTICE KENNEDY', 'MR. MCNULTY')
# print speaker_pair_coordination(('JUSTICE KENNEDY', 'MR. MCNULTY'), speaker_pairs[('JUSTICE KENNEDY', 'MR. MCNULTY')])
# print (('JUSTICE BREYER', 'MR. BAKER'))
# print speaker_pair_coordination(('JUSTICE BREYER', 'MR. BAKER'), speaker_pairs[('JUSTICE BREYER', 'MR. BAKER')])
# print speaker_pairs
print coordination_features(speaker_pairs)

######Sanity Check#########
# Pair: ('JUSTICE KENNEDY', 'MR. MCNULTY')
# 		(0, 1, 2, 2, 2, 1, 0, 0)
# 		(1, 3, 2, 0, 1, 0, 2, 0)
# 		(1, 2, 0, 1, 0, 0, 4, 1)
# 		(0, 0, 0, 0, 1, 0, 0, 0)
# 		(0, 1, 1, 0, 1, 0, 0, 0)
# 		(3, 5, 2, 1, 1, 0, 2, 0)
# 		(0, 0, 0, 0, 0, 0, 0, 0)
# 		(2, 2, 0, 2, 1, 0, 2, 0)

# cond: 	(0, 2, 2, 0, 2, 0, 0, 0)
# exhib:	(3, 3, 2, 2, 4, 0, 3, 0)
# p1cts:	(1, 3, 2, 2, 2, 1, 1, 0)

# prob:

# cond: 	(0,   2/3, 2/2, 0,   1,     0,   0, 0)
# exhib:	(3/4, 3/4, 2/4, 2/4, 4/4, 0/4, 3/4, 0/4)

# c:		(-3/4, -1/12, 1/2, -1/2, 0, 0, -1/4, 0)
