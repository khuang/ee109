
import matplotlib.pyplot as plt
import numpy as np
import random
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
random.seed(0)
scrambled_data = list(zip(iris.data, iris.target))
random.shuffle(scrambled_data)
train = scrambled_data[:100]
test = scrambled_data[100:]

num_tests = 50
successes = 0
k = 2
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

print(str(successes)+" sucessful characterizations")
print(str(num_tests-successes)+" failed characterizations")
print(str(100* successes / num_tests)+"% accurate")

#then, an optimized implementation
