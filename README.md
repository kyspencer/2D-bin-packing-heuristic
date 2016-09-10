# 2D-bin-packing-heuristic
This repo contains a 2D bin packing strategy that is based on two greedy heuristics.
This is my interpretation of Dahmani et. al. "Self-adaptive metaheuristics for solving
a multi-objective 2-dimensional vector packing problem," *Applied Soft Computing* (2014).
It can be used by itself or in conjunction with an optimization algorithm. 

The included code was written for the bin packing problem of sorting ideal two-dimensional items 
into larger bins. Each small item has a unique weight and a height associated with it. The larger
bins all have the same maximum weight and height allowance, as shown in the figure below.

![2D Bin Packing Problem](https://cloud.githubusercontent.com/assets/20876870/17501716/9de0b3a6-5daf-11e6-856d-c4df9c0df9ad.png)

My problem is a multi-objective problem where one of the objectives is to minimize the number
of bins used. The number of bins used in each solution can vary as there are other objectives 
to satisfy. The code takes a list of small item indices, such as:
```
genes = [1, 2, ..., N]
```
and translates it into an x and y matrix, as shown in the figure below.

![LoadingMatrices](https://cloud.githubusercontent.com/assets/20876870/18411732/9b1cda68-774b-11e6-8610-a693d4f74628.png)

Here, N is the total number of small items to be sorted, and M is the theoretical maximum number 
of larger bins needed. The i-indices relate to individual bins, and the j-indices relate to 
individual small items. The x-matrix shows where each item is located, and the y-matrix indicates
which bins are in use.

In the python script, it is assumed that each item was assigned a number from 1 to N.

For binpacking.py to work, you need an input file containing a list of items. The example 
included in the example folder contains 500 items. The first line indicates the max. weight
and height of a bin, and then each line after that is a weight and height for a given item. The
example file was generated using 2DCPackGen.
The items.py file creates item objects from an Item class, and the constraints.py file
checks to make sure a given packing does not violate the constraints.
