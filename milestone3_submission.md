# Milestone 3 Submission

## Performance numbers
After optimization, we classified 15 test points in X cycles, with a classification accuracy of X.

Our resource utilization was:
```bash
# Please attach your report here
```

## Design Choices

First, we got our baseline performance, with all data types as 32-bit fixed point numbers, no parallelization, the Manhattan distance, and a simple sorting tree. Our Spatial simulation achieved the following classification accuracy:

```
classification
2 0 2 2 2 1 2 0 0 2 0 0 0 1 2
gold
2 0 2 2 2 1 1 0 0 2 0 0 0 1 2
accuracy
14/15
0.933319091796875
```

Our VCS simulation ran in 92724 cycles, and had the following resource utilization:

```
```

We looked at three main ways to improve speed, resource utilization, and classification accuracy: lowering bit-precision, increasing parallelization, and changing the algorithm itself.

For the iris dataset, we only have three possible labels, and have relatively low precision data points; thus, we can use significantly fewer bits for both our labels and our data points. This saves on SRAM usage and also yields smaller logic units, decreasing resource utilization.

```
```

Our base implementation used k reduction trees, performed sequentially, to find the k nearest neighbors to our test data point. We compared that to a mergesort, which could potentially allow for better runtime at the cost of more resource utilization, due to it sorting the whole list rather than finding just the lowest k elements.

```
```

We also investigated different distance metrics (Euclidean, Chebyshev, and Manhattan) to determine which resulted in the highest accuracy and the lowest resource utilization.

```
```

Finally, we experimented with different parallelization values to find a good compromise between runtime and resource utilization.

```
```
