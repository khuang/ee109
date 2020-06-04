
import matplotlib.pyplot as plt
import numpy as np
import random
import time
from sklearn import datasets
from sklearn.decomposition import PCA

#setup stuff
iris = datasets.load_iris()

x = iris.data
y = iris.target

print(np.max(x))
print(np.min(x))
