# EE109 Final Project Proposal

## Introduction

For our project, we will be accelerating the K Nearest Neighbors machine learning algorithm. We will be using a dataset on iris plants with four features: sepal length, sepal width, petal length, and petal width. We will then use these features to characterize the class of the Iris in one of three classes(Iris SEtosa, Iris Versicolour, Iris Virginica).

## Literature Survey

Multiple groups have implemented k-Nearest Neighbors on FPGAs in the past. Both Pu et. al [1] and Tian et. al[2] use a highly parallelized set of distance calculation elements, as the distance calculations can be fully parallelized. However, these sources differ in their method of sorting the distances to determine the k nearest neighbors. Pu et. al use a bubble sort, an algorithm that is simple to implement, but generally has poor performance on real-world tasks. Tian et al. use a predetermined range sort, which offers better efficiency, but limits the maximum value of k based on the hardware implementation.

We are considering using a sorting technique described by Usui et. al [3], which uses a merge sorter tree to perform sort an entire list efficiently.

## Project Description

## Measure

## Planning


## References
[1] Y. Pu, J. Peng, L. Huang and J. Chen, "An Efficient KNN Algorithm Implemented on FPGA Based Heterogeneous Computing System Using OpenCL," 2015 IEEE 23rd Annual International Symposium on Field-Programmable Custom Computing Machines, Vancouver, BC, 2015, pp. 167-170.

[2] Miren Tian, Xin'an Wang, Xing Zhang, Zhiqiang Yang, Jipan Huang and Hao Chen, "The implementation of a KNN classifier on FPGA with a parallel and pipelined architecture based on Predetermined Range Search," 2016 13th IEEE International Conference on Solid-State and Integrated Circuit Technology (ICSICT), Hangzhou, 2016, pp. 1491-1493.

[3] T. Usui, T. V. Chu and K. Kise, "A Cost-Effective and Scalable Merge Sorter Tree on FPGAs," 2016 Fourth International Symposium on Computing and Networking (CANDAR), Hiroshima, 2016, pp. 47-56.
