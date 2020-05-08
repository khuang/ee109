
import matplotlib.pyplot as plt
import numpy as np
import random
import time
from sklearn import datasets
from sklearn.decomposition import PCA

#first, a simple manual implementation

def distance(x, y, type):
	distance = 0.0
	if type == "euclidian":
		for i in range(len(x)):
			distance += (x[i] - y[i])**2
		return np.sqrt(distance)
	if type == "manhattan":
		for i in range(len(x)):
			distance += abs(x[i] - y[i])
		return distance
	# if type == "chebyshev":
	# 	for i in range(len(x))

iris = datasets.load_iris()

num_tests = 50

random.seed(0)
scrambled_data = list(zip(iris.data, iris.target))
random.shuffle(scrambled_data)
train = scrambled_data[:(len(iris.data)-50)]
test = scrambled_data[(len(iris.data)-50):]

all_rates = {}
all_times = {}
ks = range(1,25)
distance_types = ["euclidian", "manhattan", "chebyshev"]

for type in distance_types:
	rates = []
	times = []
	for k in ks:
		successes = 0
		start_time = time.time()
		for x1, y1 in test:
			dists = []
			for x2, y2 in train:
				dist = distance(x1, x2, type)
				dists.append((dist, y2))
			dists.sort() #not sure what sort this uses
			_, neighbors = zip(*dists[0:k])
			label = max(set(neighbors), key=neighbors.count)
			if label == y1:
				successes+=1
		time_elapsed = time.time() - start_time
		times.append(time_elapsed)
		rates.append(successes/num_tests)
	all_rates[type] = rates
	all_times[type] = times

for type in distance_types:
	plt.plot(ks, all_rates[type], label=type)
plt.xlabel("K Value")
plt.ylabel("Successs Rate")
plt.legend()
plt.show()
for type in distance_types:
	plt.plot(ks, all_times[type], label=type)
plt.xlabel("K Value")
plt.ylabel("Runtime")
plt.legend()
plt.show()

#then, an optimized implementation
