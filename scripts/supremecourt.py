from __future__ import division
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
from sklearn import cross_validation
from sklearn import metrics

import sys
import os
import readdata
import utils
import numpy
import collections


high = 1
low = 0
error = 2

def bag_of_words():
	pass	


def stylistic_features(all_speaker_pairs):	
	data = []
	data_target = []
	for pair, conversation in speaker_pairs.iteritems():
		this_vector = []
		replies_x = get_replies(pair[0], conversation)
		replies_y = get_replies(pair[1], conversation)

		avg_x = len(utils.tokenize_utterance(replies_x)) / len(conversation) ##using future import above to have float number out of int division
		avg_y = len(utils.tokenize_utterance(replies_y)) / len(conversation)
	
		x_marker_count = utils.get_liwc_counts_from_utterance(replies_x)
		y_marker_count = utils.get_liwc_counts_from_utterance(replies_y)

		this_vector.append(x_marker_count)
		this_vector.append(avg_x)
		this_vector.append(avg_y)
		this_vector.append(y_marker_count)

		data.append(this_vector)

		x = all_utterances[conversation[0]]
        y = all_utterances[conversation[1]]
        if x['is_justice'] and not y['is_justice']:
            label = high
        elif not x['is_justice'] and y['is_justice']:
            label = low

        data_target.append(label);

    return (data, data_target)


def coordination_features():
	print "Takes about ~2 min to finish.....grab a cup of coffee"
	print "............................................................."
	print "raw_coord_scores"
	supreme_raw = build_raw_score(small_speaker_pairs)
	print supreme_raw

	print "............................................................."
	print "reformat into by speaker dictionary"
	pair_dictionary = build_scores_by_person(supreme_raw)

	print "............................................................."
	print "with aggregate1"
	final_score = compute_aggregate1(pair_dictionary)

	print "............................................................."
	print "adding labels"
	supreme_data, supreme_label = generate_scores_labels(final_score)
	return (supreme_data, supreme_label)

def generate_scores_labels(scores):
	final_scores = []
	scores_labels = []
	for person, its_partners in scores.iteritems():
		label = error
		pair = (person, its_partners.iterkeys().next())
		# print "      " + str(pair)
		conversation = speaker_pairs[pair]
		main_person = person
		main_utterance = all_utterances[conversation[0][0]]
		for speaking_to, pair_score in its_partners.iteritems():
			speaking_to_utterance = all_utterances[conversation[0][1]]
			if main_utterance['is_justice'] and not speaking_to_utterance['is_justice']:
				label = high
			elif not main_utterance['is_justice'] and speaking_to_utterance['is_justice']:
				label = low
			if pair_score[-1] != 'd' and label != error:
				final_scores.append(pair_score)
				scores_labels.append(label)

	print "Total Pairs: " + str(len(scores_labels))
	return(final_scores, scores_labels)


def build_raw_score(all_speaker_pairs):
	raw_coord_scores = {}
	for pair, conversation in all_speaker_pairs.iteritems():
		# print pair
		# print conversation
		curr_score = speaker_pair_coordination(pair, conversation)
		raw_coord_scores[pair] = curr_score
	# print raw_coord_scores
	return raw_coord_scores

def sum_vectors(partners_dict):
##input: dictionary of person->score
	sum_vector = (0,0,0,0,0,0,0,0)

	for person, score in partners_dict.iteritems():
		sum_vector = tuple(numpy.array(sum_vector) + numpy.array(score))

	return sum_vector

def compute_aggregate1(raw_coord_scores):

	for person, its_partners in raw_coord_scores.iteritems():
		# print person
		# for speaking_to, score in its_partners.iteritems():
		# 	print "		" + speaking_to + " " + str(score)
		person_sum = sum_vectors(its_partners)
		# print person
		# print person_sum
		person_sum = list(person_sum)
		average = 0.0
		if all(i != 0.0 for i in person_sum):
			# print sum(person_sum)
			# print len(person_sum)
			average = sum(person_sum)/len(person_sum)
		else:
			average = -20		
		# print "average: " + str(average)
		for speaking_to in its_partners:
			scores = list(its_partners[speaking_to])
			# print scores
			if average != -20:
				scores.append(average)
			else:
				scores.append('d')
			its_partners[speaking_to] = scores  

	coord_scores = raw_coord_scores
	return coord_scores

def speaker_pair_coordination(speaker_pair, conversation):
	# print speaker_pair
	b_speaker = speaker_pair[1]
	a_target = speaker_pair[0]

	b_coord_a_counts = (0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0)
	b_exhibits_counts = (0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0)
	a_exhibits_counts = (0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0)

	for exchange in conversation:
		# print exchange
		curr_coord = count_coordination(exchange)
		if curr_coord == None:
			# print "too long" 
			continue	
		b_coord_a_counts = tuple(numpy.array(b_coord_a_counts) + numpy.array(curr_coord))
		
		b_curr_exhibits = count_exhibits_feature(exchange, 1)
		a_curr_exhibits = count_exhibits_feature(exchange, 0)

		b_exhibits_counts = tuple(numpy.array(b_exhibits_counts) + numpy.array(b_curr_exhibits))
		a_exhibits_counts = tuple(numpy.array(a_exhibits_counts) + numpy.array(a_curr_exhibits))
	# print b_coord_a_counts 
	# print b_exhibits_counts 
	# print a_exhibits_counts
	return calc_coordination(len(conversation), b_coord_a_counts, b_exhibits_counts, a_exhibits_counts)


def count_coordination(utterance_pair):
	b_utterance = all_utterances[utterance_pair[1]]['utterance']
	a_utterance = all_utterances[utterance_pair[0]]['utterance']

	b_utter_vec = utils.get_liwc_counts_from_utterance(b_utterance)
	a_utter_vec = utils.get_liwc_counts_from_utterance(a_utterance)

	tokenized_b = utils.tokenize_utterance(b_utterance)
	tokenized_a = utils.tokenize_utterance(a_utterance)

	#throw this conversation out if difference in utterance length is greater than 20 
	if abs(len(tokenized_b) - len(tokenized_a)) >=20: return None
	
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
	coordination_prob = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
	for i in xrange(0, len(coordination_counts)):
		if coordination_counts[i] == 0.0:
			coordination_prob[i] = 0.0
		else:
			coordination_prob[i] = coordination_counts[i] / a_exhibits_counts[i];

	b_exhibits_prob = tuple(numpy.array(b_exhibits_counts) / num_exchange);

	coord_prob = tuple(numpy.array(coordination_prob) - numpy.array(b_exhibits_prob))
	# print coord_prob
	return coord_prob

def build_scores_by_person(coord_raw_scores):
	"""
	{'JUSTICE STEVENS': {'MR.MCNULTY': 0.23423523, 
						 'MR.MOODY': 0.23434324}}

	"""
	all_scores_person =  collections.defaultdict(lambda:{})
	for pair, score in coord_raw_scores.iteritems():
		person_x = pair[0]
		person_y = pair[1]
		# print person_x
		# print person_y
		all_scores_person[person_x][person_y] = score
		# print all_scores_person

	return all_scores_person

def to_sklearn_format(all_scores):
	data = []
	data_target =[]
	for pair, score in all_scores.iteritems():
		data.append(list(score[1]))
		data_target.append(score[0])

	return data, data_target

def svm_cv(data, data_target, extract_features):
	X_train, X_test, y_train, y_test = cross_validation.train_test_split(data, data_target)
	if (extract_features):
		print "Extracting features"
   	 	vectorizer = TfidfVectorizer(norm = 'l2')
    	X_train = vectorizer.fit_transform(data_train)
    	print len(vectorizer.get_feature_names())
    	X_test = vectorizer.transform(data_test)

	print "Training..."
	clf = svm.LinearSVC()
	clf.fit(X_train, y_train)
	print "Testing..."
	pred = clf.predict(X_test)
	accuracy_score = metrics.accuracy_score(y_test, pred)
	classification_report = metrics.classification_report(y_test, pred)
	print accuracy_score
	print classification_report
	numpy.set_printoptions(threshold='nan')
	print y_test
	print pred

# ========================== MAIN STARTS HERE ===================== #

all_utterances, speaker_pairs = readdata.read_supreme_court()
print "............................................................."
print ""
print "Original # of Speaker Pairs: " + str(len(speaker_pairs))

# supreme_cf, supreme_target_cf = coordination_features()
# print "==========COORDINATION FEATURES================="
# svm_cv(supreme, supreme_target, extract_features = false)


# supreme_bow, supreme_target_bow = bag_of_words()
# print "==========BAG OF WORDS FEATURES================="
# svm_cv(supreme_bow, supreme_target_bow, extract_features = false)

# supreme_bow, supreme_target_bow = stylistic_features()
# print "==========STYLISTIC FEATURES================="
# svm_cv(supreme_bow, supreme_target_bow)

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

small_speaker_pairs ={
('JUSTICE SOUTER', 'MR. COLEMAN'): [(5416, 5417), (5418, 5419), (5448, 5449), (5450, 5451), (5479, 5480), (5481, 5482), (5483, 5484), (5485, 5486), (5487, 5488), (5489, 5490), (40634, 40635), (40636, 40637), (40638, 40639), (40640, 40641)],
("JUSTICE O'CONNOR", 'MS. NIELD'): [(25592, 25593), (25594, 25595), (25605, 25606), (25607, 25608), (25609, 25610), (25622, 25623), (25624, 25625), (25626, 25627), (25663, 25664), (25665, 25666), (25667, 25668), (25669, 25670), (25671, 25672), (25673, 25674), (25675, 25676), (25677, 25678), (25679, 25680), (25681, 25682), (25683, 25684)], 
('MS. SULLIVAN', 'JUSTICE KENNEDY'): [(1130, 1131), (1132, 1133), (1134, 1135), (1182, 1183), (1184, 1185), (1191, 1192), (1193, 1194), (1195, 1196), (1203, 1204), (16531, 16532)], 
('JUSTICE SOUTER', 'MR. ENGLERT'): [(32095, 32096), (32097, 32098)], 
('CHIEF JUSTICE ROBERTS', 'CHIEF JUSTICE ROBERTS'): [(13618, 13619), (14215, 14216), (15065, 15066), (23364, 23365), (31246, 31247), (31770, 31771), (42356, 42357), (48454, 48455)], 
('JUSTICE STEVENS', 'MR. KASNER'): [(17753, 17754), (17755, 17756), (17757, 17758), (17778, 17779), (17780, 17781), (17782, 17783), (17784, 17785), (17786, 17787), (17788, 17789), (17790, 17791), (17793, 17794), (18039, 18040), (18041, 18042)], 
('MR. ZAS', 'JUSTICE SOUTER'): [(44175, 44176), (44177, 44178), (44179, 44180), (44181, 44182), (44183, 44184), (44185, 44186), (44187, 44188), (44197, 44198), (44201, 44202), (44204, 44205)], 
('JUSTICE GINSBURG', 'MS. MADIGAN'): [(10032, 10033), (10111, 10112)], 
('JUSTICE STEVENS', 'MR. JONES'): [(9461, 9462), (9463, 9464), (9465, 9466), (9467, 9468), (9479, 9480), (9481, 9482), (9483, 9484), (9488, 9489), (9490, 9491), (9492, 9493), (38807, 38808), (38809, 38810), (38811, 38812), (38813, 38814), (38821, 38822)]
}