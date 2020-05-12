# EE109 Final Project Proposal

Zachary Belateche and Kathy Huang

## Introduction

For our project, we will be accelerating the K Nearest Neighbors machine learning algorithm. We will be using a dataset on iris plants with four features: sepal length, sepal width, petal length, and petal width. We will then use these features to characterize the class of the Iris in one of three classes(Iris SEtosa, Iris Versicolour, Iris Virginica). The dataset can be found at: https://archive.ics.uci.edu/ml/datasets/iris.

## Literature Survey

Multiple groups have implemented k-Nearest Neighbors on FPGAs in the past. Both Pu et. al [1] and Tian et. al[2] use a highly parallelized set of distance calculation elements, as the distance calculations can be fully parallelized. However, these sources differ in their method of sorting the distances to determine the k nearest neighbors. Pu et. al use a bubble sort, an algorithm that is simple to implement, but generally has poor performance on real-world tasks. Tian et al. use a predetermined range sort, which offers better efficiency, but limits the maximum value of k based on the hardware implementation.

We are considering using a sorting technique described by Usui et. al [3], which uses a merge sorter tree to perform sort an entire list efficiently.

## Project Description

Like the results reported in literature, we plan to use a highly paralellized set of distance calculation elements. We're planning to use a sorting tree, like the one described by by Usui et. al to efficiently sort our elements to find the k nearest neighbors. A block diagram is provided in Figure 1.

![Block diagram](block_diagram.png)
**Figure 1: Block Diagram**

## Measure

We will be measuring the quality of our design through multiple metrics. Primarily, we will be looking at raw performance through cycle counts. However, to have a more nuanced measurement, we will also look at resource utilization and make sure that we are using resources effectively (and not underutilizing resources). By considering both measurements, we will have a more robust idea of our design's performance.

## Planning

1. Software Simulation (Milestone 1 due May 11)
    * We are planning to complete the software simulation for this project by the first project milestone of May 18. For the software simulation, we are planning to implement KNN and play around to determinethe best distance function and the value of k to use for our project.
2. Hardware Simulation (Milestone 2 due May 20)
    * We will complete the initial hardware simulation by the milestone date of May 27. This will primarily be our first stage of hardware implementation and will optimize this implementation for performance in the next stage of the project.
3. Hardware Deployment (Milestone 3 due June 8)
    * Since we will not be able to deploy our project on hardware this quarter, for this milestone we will focus on improving our design's performance.
4. Report on Findings (Final Report due June 10)

## References
[1] Y. Pu, J. Peng, L. Huang and J. Chen, "An Efficient KNN Algorithm Implemented on FPGA Based Heterogeneous Computing System Using OpenCL," 2015 IEEE 23rd Annual International Symposium on Field-Programmable Custom Computing Machines, Vancouver, BC, 2015, pp. 167-170.

[2] Miren Tian, Xin'an Wang, Xing Zhang, Zhiqiang Yang, Jipan Huang and Hao Chen, "The implementation of a KNN classifier on FPGA with a parallel and pipelined architecture based on Predetermined Range Search," 2016 13th IEEE International Conference on Solid-State and Integrated Circuit Technology (ICSICT), Hangzhou, 2016, pp. 1491-1493.

[3] T. Usui, T. V. Chu and K. Kise, "A Cost-Effective and Scalable Merge Sorter Tree on FPGAs," 2016 Fourth International Symposium on Computing and Networking (CANDAR), Hiroshima, 2016, pp. 47-56.
