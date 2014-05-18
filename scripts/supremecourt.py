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
		svm_vector.append(speaker_pair_coordination(pair, conversation))
		allscores[pair] = svm_vector
		# print allscores[pair]

	return allscores


# svm_vector = [0] * 10
#     	label = error
#     	if (pair[0].find('JUSTICE') > -1 and pair[1].find('JUSTICE') == -1):
#     		label = high
#     	if (pair[0].find('CHIEF') > -1 and pair[1].find('CHIEF') == -1):
#     		label = high
#     	else:
#     		label = low
#     	svm_vector.append(str(pair))
#     	svm_vector.append(label)
#     	print svm_vector
    	# C_score = tuple(speaker_pair_coordination(pair, conversation))
    	# svm_vector.append(C_score)
    	# allscores[pair] = svm_vector



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
