import csv
from sklearn import datasets
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics


iris = datasets.load_iris()
x = iris.data
y = iris.target

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.1, random_state = 4)

with open('iris.csv', mode='w') as csv_file:
    writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    # writer.writerow([len(x_train)])
    for xtr in x_train:
        writer.writerow(xtr)

    for ytr in y_train:
        writer.writerow([ytr])

    # writer.writerow([len(x_test)])
    for xtr in x_test:
        writer.writerow(xtr)

    for ytr in y_test:
        writer.writerow([ytr])
