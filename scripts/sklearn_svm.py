import random
import sklearn
from sklearn import svm
from sklearn.datasets import load_svmlight_file


markers = ["articles", "auxverbs", "conj", "highfreq_adverbs", "ipronouns", "ppronouns", "prep", "quant"]
markers_int = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
# markers = set(markers)

##
##



def svm_train(train_scores_filename, name):
	print "Training SVM for " + name + " ..."
	all_vectors= []
	for pair, score in train_scores:
		c_score = numpy.array(score[1])
		vector = "" + str(score[0])

		for marker in markers_int:
			s = '%(markertype)s:%(value)f' % \
				{"markertype": marker, "value": score[1][marker]}
			vector += s + ' '
		all_vectors.append(vector)
	svm_write_to_file(name, all_vectors)

# def svm_predict():
def svm_read_from_file(filename):
	vector_samples = []
	f = open(filename, 'r')
	line = f.readline()
	line = line.split(' \[]')
	vector_samples.append(line)
	return vector_samples

def svm_write_to_file(filename_output, vectors):
	f = open('filename_output', 'w')
	for vector in vector_file:
		f.write(sample)
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

	f = open('svm_test', 'w')
	for sample in sample_vectors:
		f.write(sample)
		f.write('\n')

	f.close()

X_train, y_train = load_svmlight_file('svm_test')

clf = svm.SVC()
clf.fit(X_train,y_train)


# print clf.predict([0.472878, 0.344089, 0.636890, 0.311382, 0.348450, 0.040245, 0.668857, 0.365363, 0.436143, 0.478268])


print svm_read_from_file(testoutput)