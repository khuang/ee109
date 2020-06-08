
import matplotlib.pyplot as plt
import numpy as np
import random
import time
from sklearn import datasets
from sklearn.decomposition import PCA

#first, a simple manual implementation

#multiple defined distance metrics
def distance(x, y, type):
	distance = 0.0
	#euclidian distance: (sqrt(x^2 + y^2))
	if type == "euclidian":
		for i in range(len(x)):
			distance += (x[i] - y[i])**2
		return distance
	#manhattan distance
	if type == "manhattan":
		for i in range(len(x)):
			distance += abs(x[i] - y[i])
		return distance
	#chebyshev / checkerboard distance
	#the longest distance along a dimensions
	if type == "chebyshev":
		for i in range(len(x)):
			d = abs(x[i] - y[i])
			if d > distance:
				distance = d
		return distance

#classify x based on the training set and k
def knn_classify(x, train, k):
	dists = []
	for x2, y2 in train:
		dist = distance(x, x2, type)
		dists.append((dist, y2))
	dists.sort() #not sure what sort this uses
	_, neighbors = zip(*dists[0:k])
	label = max(set(neighbors), key=neighbors.count)
	return label

#setup stuff
iris = datasets.load_iris()
num_tests = 10
all_rates = {}
all_times = {}
ks = range(1,20)
distance_types = ["euclidian", "manhattan", "chebyshev"]
seeds = range(1,2)

#try different distance metrics
for type in distance_types:

	type_rates = [0]*len(ks)
	type_times = [0]*len(ks)

	for seed in seeds:
		#randomly pick which 10 we want to use as test data
		random.seed(seed)
		scrambled_data = list(zip(iris.data, iris.target))
		random.shuffle(scrambled_data)
		train = scrambled_data[:(len(iris.data)-num_tests)]
		test = scrambled_data[(len(iris.data)-num_tests):]

		rates = []
		times = []

		#try different k's
		for k in ks:
			successes = 0
			start_time = time.time()

			#try for all test elements
			for x1, y1 in test:
				label = knn_classify(x1, train, k)
				if label == y1:
					successes+=1

			#save data
			time_elapsed = time.time() - start_time
			times.append(time_elapsed)
			rates.append(successes/num_tests)

		#average the data together
		for i in range(len(rates)):
			type_rates[i] = (rates[i] * (1/seed)) + (type_rates[i] * ((seed-1)/seed))
			type_times[i] = (times[i] * (1/seed)) + (type_times[i] * ((seed-1)/seed))

	all_rates[type] = type_rates
	all_times[type] = type_times

#then, an optimized implementation
x = iris.data
y = iris.target

# random.seed(0)
# scrambled_data = list(zip(iris.data, iris.target))
# random.shuffle(scrambled_data)
# x,y = zip(*scrambled_data)

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.1, random_state = 4)

scores = []
times = []
res = []
import pyRAPL
for k in ks:
	pyRAPL.setup()
	start_time = time.time()
	meter = pyRAPL.Measurement('bar')
	meter.begin()
	knn = KNeighborsClassifier(n_neighbors=k, n_jobs=1)
	knn.fit(x_train, y_train)
	y_pred=knn.predict(x_test)
	time_elapsed = time.time() - start_time
	meter.end()
	res.append(meter.result.pkg[0])
	times.append(time_elapsed)
	scores.append(metrics.accuracy_score(y_test, y_pred))

print(np.mean(times))
print(str(np.mean(res)) + " uJ")

#plot the data
for type in distance_types:
	plt.plot(ks, all_rates[type], label=type)

plt.plot(ks, scores, label = "sklearn")
plt.xlabel("K Value")
plt.ylabel("Successs Rate")
plt.legend()
plt.show()

for type in distance_types:
	plt.plot(ks, all_times[type], label=type)
plt.plot(ks, times, label = "sklearn")
plt.xlabel("K Value")
plt.ylabel("Runtime")
plt.legend()
plt.show()
