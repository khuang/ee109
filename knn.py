
import matplotlib.pyplot as plt
import numpy as np
import random
import time
from sklearn import datasets
from sklearn.decomposition import PCA

#first, a simple manual implementation

def distance(x, y): #using euclidian for now at least
	distance = 0.0
	for i in range(len(x)-1):
		distance += (x[i] - y[i])**2
	return np.sqrt(distance)

iris = datasets.load_iris()

#scramble the data

num_tests = 50

random.seed(0)
scrambled_data = list(zip(iris.data, iris.target))
random.shuffle(scrambled_data)
train = scrambled_data[:(len(iris.data)-50)]
test = scrambled_data[(len(iris.data)-50):]

rates = []
times = []
ks = range(1,25)
for k in ks:
	successes = 0
	start_time = time.time()
	for x1, y1 in test:
		dists = []
		for x2, y2 in train:
			dist = distance(x1, x2)
			dists.append((dist, y2))
		dists.sort() #not sure what sort this uses
		_, neighbors = zip(*dists[0:k])
		label = max(set(neighbors), key=neighbors.count)
		if label == y1:
			successes+=1
	time_elapsed = time.time() - start_time
	times.append(time_elapsed)
	rates.append(successes/num_tests)

plt.plot(ks, rates)
plt.xlabel("K Value")
plt.ylabel("Successs Rate")
plt.show()
plt.plot(ks, times)
plt.xlabel("K Value")
plt.ylabel("Runtime")
plt.show()

#then, an optimized implementation
