from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
from sklearn import cross_validation
from sklearn import metrics

import sys
import os
import readdata
import utils
import numpy

markers = ["articles", "auxverbs", "conj", "highfreq_adverbs", "ipronouns", "ppronouns", "prep", "quant"]
markers_int = ["1", "2", "3", "4", "5", "6", "7", "8"]
# markers = set(markers)

##
#
def svm_train(train_scores_filename, outputfile_name):
	print "Training SVM for " + outputfile_name + " ..."
	all_vectors= svm_read_from_file(train_scores_filename)

	svm_vectors = []
	for vector in all_vectors:
		svm_vector = "" + str(int(vector[0])) + ' '
		i = 1
		for marker in markers_int:
			s = '%(markertype)s:%(value)f' % \
				{"markertype": marker, "value": float(vector[i])}
			svm_vector += s + ' '
			i += 1
		svm_vectors.append(svm_vector)
	outputfile = outputfile_name + '.svmout'
	svm_write_to_file(outputfile, svm_vectors)

def svm_prep_test(test_data_file):
	print "Sanitizing test data...."
	all_vectors= svm_read_from_file(test_data_file)

	svm_test_allvectors = []
	for vector in all_vectors:
		svm_test_vector = []
		# float_values = map(lambda x: float(x), vector)
		for i in range(0, len(vector)):
			svm_test_vector.append(float(vector[i]))
		# print svm_test_vector
		svm_test_allvectors.append(svm_test_vector)
		
	# outputfile = outputfile_name + '.svmtest'
	# svm_write_to_file(outputfile, svm_test_allvectors)
	# print svm_test_allvectors
	return svm_test_allvectors

def svm_predict(train_data_file, test_data_file):
	accuracy = 0.0
	numTotal = 0.0
	numHigh = 0.0
	goldHigh = 0.0
	X_train, y_train = load_svmlight_file(train_data_file)
	clf = svm.SVC()
	clf.fit(X_train,y_train)

	test_data_list = svm_prep_test(test_data_file)

	for test_data in test_data_list:
		just_test = test_data[1:]
		prediction = clf.predict(just_test)
		# print "sample: " + str(test_data)
		# print "prediction " + str(prediction)
		if prediction > 0: numHigh += 1
		if test_data[0] > 0: goldHigh +=1
		numTotal += 1

def svm_cv(data, data_target):
	data_train, data_test, y_train, y_test = cross_validation.train_test_split(data, data_target)
    print "Extracting features"
    vectorizer = TfidfVectorizer(norm = 'l2')
    X_train = vectorizer.fit_transform(data_train)
    print len(vectorizer.get_feature_names())
    X_test = vectorizer.transform(data_test)
    print "Training"
    clf = svm.LinearSVC()
    clf.fit(X_train, y_train)
    print "Testing"
    pred = clf.predict(X_test)
    accuracy_score = metrics.zero_one_score(y_test, pred)
    classification_report = metrics.classification_report(y_test, pred)
    print accuracy_score
    print classification_report
    numpy.set_printoptions(threshold='nan')
    print y_test
    print pred


# def find_accuracy():

def svm_read_from_file(filename):
	##output is a vector of string values
	f = open(filename, 'rb')
	lines = f.readlines()
	f.close()
	vector_samples = []

	for line in lines:
		newline = re.sub(r'[\[\]:,\n]', '', line)
		vector = newline.split(' ')
		# print vector
		vector_samples.append(vector)
	return vector_samples

def svm_write_to_file(filename_output, vectors):
	f = open(filename_output, 'w')
	for vector in vectors:
		f.write(vector)
		f.write('\n')
	f.close()

# def svm_test():
# 	##generate generate random vectors
# 	sample_vectors = [];
# 	for i in xrange(0, 10):
# 		sample = "" + random.choice('01') + ' '

# 		for marker in markers_int:
# 			value = random.uniform(0,1)
# 			s = '%(markertype)s:%(value)f' % \
# 				{"markertype": marker, "value": value}
# 			sample += s + ' '
# 		sample_vectors.append(sample);

# 	# print sample_vectors

# 	f = open('svm_test', 'wb')
# 	for sample in sample_vectors:
# 		f.write(sample)
# 		f.write('\n')

# 	f.close()

# X_train, y_train = load_svmlight_file('svm_test')

# clf = svm.SVC()
# clf.fit(X_train,y_train)


# print clf.predict([0.472878, 0.344089, 0.636890, 0.311382, 0.348450, 0.040245, 0.668857, 0.365363, 0.436143, 0.478268])


# vectorarray = svm_read_from_file('testoutput')
# print vectorarray
# svm_train('supremecourt_train', 'supremecourt_train')
# svm_predict('supremecourt_train.svmout', 'supremecourt_train')



# print ""
# print vectorarray[0].split('[')
# print vectorarray[1].split('[')
# print vectorarray[2].split('[')
# print vectorarray[3].split('[')
