# Milestone 3 Submission

## Performance numbers
After optimization, we classified 15 test points in X cycles, with a classification accuracy of 93.33%.

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
+--------------------------------------+-------+-------+-----------+-------+
|               Site Type              |  Used | Fixed | Available | Util% |
+--------------------------------------+-------+-------+-----------+-------+
| Slice LUTs                           | 43632 |     0 |    218600 | 19.96 |
|   LUT as Logic                       | 29858 |     0 |    218600 | 13.66 |
|   LUT as Memory                      |  5006 |     0 |     70400 |  7.11 |
|     LUT as Distributed RAM           |  3076 |     0 |           |       |
|     LUT as Shift Register            |  1930 |     0 |           |       |
|   LUT used exclusively as pack-thrus |  8768 |     0 |    218600 |  4.01 |
| Slice Registers                      | 49044 |     0 |    437200 | 11.22 |
|   Register as Flip Flop              | 49039 |     0 |    437200 | 11.22 |
|   Register as Latch                  |     0 |     0 |    437200 |  0.00 |
|   Register as pack-thrus             |     5 |     0 |    437200 | <0.01 |
| F7 Muxes                             |  1282 |     0 |    109300 |  1.17 |
| F8 Muxes                             |   256 |     0 |     54650 |  0.47 |
+--------------------------------------+-------+-------+-----------+-------+
```

**We looked at three main ways to improve speed, resource utilization, and classification accuracy: lowering bit-precision, increasing parallelization, and changing the algorithm itself.**

We started by investigating different distance metrics (Euclidean, Chebyshev, and Manhattan) to determine which resulted in the highest accuracy and the lowest resource utilization.

Our base implementation used the Manhattan distance, and achieved 93% classification accuracy, in 92724 cycles, with the resource utilization above. Using the Chebyshev distance gave the same classification accuracy (93%), a runtime of 97256 cycles, and a resource utilization of:
```
+--------------------------------------+-------+-------+-----------+-------+
|               Site Type              |  Used | Fixed | Available | Util% |
+--------------------------------------+-------+-------+-----------+-------+
| Slice LUTs                           | 43382 |     0 |    218600 | 19.85 |
|   LUT as Logic                       | 29764 |     0 |    218600 | 13.62 |
|   LUT as Memory                      |  5004 |     0 |     70400 |  7.11 |
|     LUT as Distributed RAM           |  3076 |     0 |           |       |
|     LUT as Shift Register            |  1928 |     0 |           |       |
|   LUT used exclusively as pack-thrus |  8614 |     0 |    218600 |  3.94 |
| Slice Registers                      | 48970 |     0 |    437200 | 11.20 |
|   Register as Flip Flop              | 48965 |     0 |    437200 | 11.20 |
|   Register as Latch                  |     0 |     0 |    437200 |  0.00 |
|   Register as pack-thrus             |     5 |     0 |    437200 | <0.01 |
| F7 Muxes                             |  1282 |     0 |    109300 |  1.17 |
| F8 Muxes                             |   256 |     0 |     54650 |  0.47 |
+--------------------------------------+-------+-------+-----------+-------+
```
This is slightly better than the Manhattan distance in all categories, likely due to the relative simplicity of using comparisons rather than additions. We also tried the Euclidean distance, which also gave us an accuracy of 93%. However, it ran in 105356 cycles, and had a resource utilization of:
```
+--------------------------------------+-------+-------+-----------+-------+
|               Site Type              |  Used | Fixed | Available | Util% |
+--------------------------------------+-------+-------+-----------+-------+
| Slice LUTs                           | 44141 |     0 |    218600 | 20.19 |
|   LUT as Logic                       | 30211 |     0 |    218600 | 13.82 |
|   LUT as Memory                      |  5357 |     0 |     70400 |  7.61 |
|     LUT as Distributed RAM           |  3076 |     0 |           |       |
|     LUT as Shift Register            |  2281 |     0 |           |       |
|   LUT used exclusively as pack-thrus |  8573 |     0 |    218600 |  3.92 |
| Slice Registers                      | 49939 |     0 |    437200 | 11.42 |
|   Register as Flip Flop              | 49876 |     0 |    437200 | 11.41 |
|   Register as Latch                  |     0 |     0 |    437200 |  0.00 |
|   Register as pack-thrus             |    63 |     0 |    437200 |  0.01 |
| F7 Muxes                             |  1282 |     0 |    109300 |  1.17 |
| F8 Muxes                             |   256 |     0 |     54650 |  0.47 |
+--------------------------------------+-------+-------+-----------+-------+
```
The Euclidian distance had the worst resource utilization across the board, likely due to the high hardware cost of multiplication. **As such, we decided to go with the Chebyshev distance as our distance metric, as it achieved the same accuracy as the other metrics while minimizing runtime and resource utilization.**

For the iris dataset, we only have three possible labels, and have relatively low precision data points; thus, we can use significantly fewer bits for both our labels and our data points. This saves on SRAM usage and also yields smaller logic units, decreasing resource utilization.

```
```

Our base implementation used k reduction trees, performed sequentially, to find the k nearest neighbors to our test data point. We compared that to a mergesort, which could potentially allow for better runtime at the cost of more resource utilization, due to it sorting the whole list rather than finding just the lowest k elements.

```
```

Finally, we experimented with different parallelization values to find a good compromise between runtime and resource utilization.

```
```