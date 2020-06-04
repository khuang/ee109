# EE109 Digital System Lab Final Report
Zach Belateche, Kathy Huang

## Table of Contents
- Application Overview
- Software Simulation
- Hardware Implementation
- Design Tradeoffs
- Appendix

## Application Overview
For our project, we accelerated the k-Nearest Neighbors machine learning algorithm. We used a dataset on iris plants with four features: sepal length, sepal width, petal length, and petal width. We used these features to characterize the iris in one of three classes (Iris SEtosa, Iris Versicolour, Iris Virginica). The dataset can be found at: https://archive.ics.uci.edu/ml/datasets/iris.

Multiple groups have implemented k-Nearest Neighbors on FPGAs in the past. Both Pu et. al [1] and Tian et. al[2] use a highly parallelized set of distance calculation elements, as the distance calculations can be fully parallelized. However, these sources differ in their method of sorting the distances to determine the k nearest neighbors. Pu et. al use a bubble sort, an algorithm that is simple to implement, but generally has poor performance on real-world tasks. Tian et al. use a predetermined range sort, which offers better efficiency, but limits the maximum value of k based on the hardware implementation.

## Software Simulation
In software, we implemented K-Nearest Neighbors on the Iris dataset using multiple distance metrics, as well as using SciKit Learn, and analyzed the performance. The simpler distance metrics (Chebyshev & Manhattan distance) offered faster run-times with comparable or better performance than the Euclidian distance.

![Performance Analysis](1.png)

**Figure 2: Accuracy vs K Value**

![Performance Analysis](2.png)

**Figure 2: Runtime vs K Value**

## Hardware Implementation
Like the implementations reported in literature, we used a highly parallelized set of distance calculation elements. We also used a predetermined range sort using k sequential reductions through a reduction tree; this yields k log(N) runtime with N log(N) resource utilization. A block diagram is provided in Figure 1.

![Block diagram](block_diagram.png)

**Figure 1: Block Diagram**

## Design Tradeoffs

*This section will basically just be milestone 3*
```
// Discuss your tradeoffs between the design choices you've made
```

## Appendix

All of our source code is located on github, at `https://github.com/khuang/ee109`.

```
// If you have any comments about the class, or have a video you want to show us,
// feel free to add them in the Appendix.
```

## References
[1] Y. Pu, J. Peng, L. Huang and J. Chen, "An Efficient KNN Algorithm Implemented on FPGA Based Heterogeneous Computing System Using OpenCL," 2015 IEEE 23rd Annual International Symposium on Field-Programmable Custom Computing Machines, Vancouver, BC, 2015, pp. 167-170.

[2] Miren Tian, Xin'an Wang, Xing Zhang, Zhiqiang Yang, Jipan Huang and Hao Chen, "The implementation of a KNN classifier on FPGA with a parallel and pipelined architecture based on Predetermined Range Search," 2016 13th IEEE International Conference on Solid-State and Integrated Circuit Technology (ICSICT), Hangzhou, 2016, pp. 1491-1493.
