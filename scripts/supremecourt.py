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

def coordination_features(all_speaker_pairs):
	#TODO Macro-Averaging C(b, A)
	print "Takes about ~2min to finish.....grab a cup of coffee"
	allscores = {}
	high = 10
	low = 0
	error = -1
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
		svm_vector.append(speaker_pair_coordination(pair, conversation))
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

def write_to_file(filename_output, all_scores):
	f = open(filename_output, 'wb')
	for pair, score in all_scores.iteritems():
		score_output = str(score[0]) + " " + str(list(score[1]))
		# print score_output
		f.write(score_output)
		f.write('\n')
	f.close()


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
supremecourt_scores = coordination_features(speaker_pairs)
write_to_file('supremecourt_train', supremecourt_scores)
# test_scores = {
# ('MR. TRIBE', 'JUSTICE KENNEDY'): [1, (-0.072463768115942018, -0.0033444816053511683, -0.049689440993788858, -0.10559006211180127, 0.047101449275362306, -0.20158102766798414, 0.030100334448160626, -0.19130434782608696)], 
# ('MR. HAGLUND', 'JUSTICE SCALIA'): [1, (-0.08333333333333337, 0.0, 0.0, 0.0, -0.16666666666666669, 0.083333333333333315, -0.08333333333333337, 0.25)], 
# ('MR. PETRO', 'CHIEF JUSTICE REHNQUIST'): [1, (-0.25, -0.5, 0.0, -0.25, 0.25, -0.08333333333333337, 0.0, 0.0)], 
# ('MS. HART', 'JUSTICE KENNEDY'): [-1, (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)], 
# ('JUSTICE KENNEDY', 'MS. PERALES'): [1, (0.0, 0.13333333333333341, -0.08333333333333337, 0.5, -0.066666666666666652, 0.0, -0.033333333333333326, 0.16666666666666666)], 
# ('MR. DREEBEN', 'JUSTICE ALITO'): [-1, (-0.023809523809523725, -0.023809523809523725, -0.057142857142857051, -0.11428571428571432, -0.023809523809523725, -0.057142857142857051, -0.023809523809523725, -0.057142857142857051)], 
# ('MR. SALMONS', 'JUSTICE STEVENS'): [1, (0.042010502625656421, 0.011627906976744207, 0.097674418604651203, 0.10570824524312894, 0.009966777408637828, 0.37388193202146697, -0.050872093023255793, 0.013953488372093037)], 
# ('MR. STEIKER', 'CHIEF JUSTICE ROBERTS'): [-1, (-0.015384615384615441, 0.070512820512820484, 0.061538461538461542, -0.067307692307692291, 0.030769230769230771, -0.18681318681318687, 0.030769230769230771, -0.23076923076923078)], ('MR. ROBBINS', 'JUSTICE STEVENS'): [1, (-0.012987012987012991, 0.056818181818181768, 0.030303030303030276, 0.11363636363636365, -0.060606060606060663, 0.030303030303030276, 0.056818181818181768, 0.39393939393939392)], ("JUSTICE O'CONNOR", 'MR. ZAGRANS'): [1, (-0.5, 0.0, -0.5, -0.5, 0.0, 0.0, 0.0, -0.5)], ('MR. JOHNSON', 'JUSTICE STEVENS'): [1, (-0.050000000000000044, -0.04166666666666663, -0.0069444444444444198, 0.0, -0.0625, 0.0625, 0.0056818181818182323, -0.25)], ('JUSTICE SOUTER', 'MR. FELDMAN'): [1, (0.044871794871794934, 0.05555555555555558, 0.31623931623931623, 0.098290598290598274, -0.045248868778280493, 0.055944055944055937, 0.20879120879120883, 0.11538461538461536)]
# }
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
