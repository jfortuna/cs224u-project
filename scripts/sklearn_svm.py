import random
import sklearn
from sklearn import svm
from sklearn.datasets import load_svmlight_file
import re

markers = ["articles", "auxverbs", "conj", "highfreq_adverbs", "ipronouns", "ppronouns", "prep", "quant"]
markers_int = ["1", "2", "3", "4", "5", "6", "7", "8"]
# markers = set(markers)

##
#
def svm_train(train_scores_filename, name):
	print "Training SVM for " + name + " ..."
	all_vectors= svm_read_from_file(train_scores_filename)

	svm_vectors = []
	for vector in all_vectors:
		svm_vector = "" + str(int(vector[0])) + ' '
		i = 1
		for marker in markers_int:
			# print vector[i]
			s = '%(markertype)s:%(value)f' % \
				{"markertype": marker, "value": float(vector[i])}
			# print s
			# print vector[i]
			svm_vector += s + ' '
			i += 1
		svm_vectors.append(svm_vector)
	outputfile = name + '.svmout'
	# print "HERSERSER"
	svm_write_to_file(outputfile, svm_vectors)

# ['1', '-0.07246376811594202', '-0.0033444816053511683', '-0.04968944099378886', '-0.10559006211180127', '0.047101449275362306', '-0.20158102766798414', '0.030100334448160626', '-0.19130434782608696\n'], ['1', '-0.015384615384615441', '0.07051282051282048', '0.06153846153846154', '-0.06730769230769229', '0.03076923076923077', '-0.18681318681318687', '0.03076923076923077', '-0.23076923076923078\n']
# 1 1:0.916128 2:0.063443 3:0.058924 4:0.340437 5:0.102476 6:0.299614 7:0.004428 8:0.557098 9:0.667828 10:0.614473
# def svm_predict():
def svm_read_from_file(filename):

	f = open(filename, 'rb')
	lines = f.readlines()
	f.close()
	vector_samples = []

	for line in lines:
		newline = re.sub(r'[\[\]:,\n]', '', line)
		vector = newline.split(' ')
		# print vector
		vector_samples.append(vector)
	# print vector_samples
	return vector_samples

def svm_write_to_file(filename_output, vectors):
	f = open(filename_output, 'w')
	for vector in vectors:
		f.write(vector)
		f.write('\n')
	f.close()

def svm_test():
	##generate generate random vectors
	sample_vectors = [];
	for i in xrange(0, 10):
		sample = "" + random.choice('01') + ' '

		for marker in markers_int:
			value = random.uniform(0,1)
			s = '%(markertype)s:%(value)f' % \
				{"markertype": marker, "value": value}
			sample += s + ' '
		sample_vectors.append(sample);

	# print sample_vectors

	f = open('svm_test', 'wb')
	for sample in sample_vectors:
		f.write(sample)
		f.write('\n')

	f.close()

X_train, y_train = load_svmlight_file('svm_test')

clf = svm.SVC()
clf.fit(X_train,y_train)


# print clf.predict([0.472878, 0.344089, 0.636890, 0.311382, 0.348450, 0.040245, 0.668857, 0.365363, 0.436143, 0.478268])


# vectorarray = svm_read_from_file('testoutput')
# print vectorarray
svm_train('testoutput', 'test')
# print ""
# print vectorarray[0].split('[')
# print vectorarray[1].split('[')
# print vectorarray[2].split('[')
# print vectorarray[3].split('[')
