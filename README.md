# 2D-bin-packing-heuristic
This repo contains a 2D bin packing strategy that is based on two greedy heuristics.
This is my interpretation of Dahmani et. al. "Self-adaptive metaheuristics for solving
a multi-objective 2-dimensional vector packing problem," *Applied Soft Computing* (2014).
It can be used by itself or in conjunction with an optimization algorithm. 

The problem for which this implementation was geared to focus on sorting ideal items
that have a weight and a height associated with them. Each bin also has a maximum weight
and a maximum height allowance. 

![alt text](https://github.com/kyspencer/2D-bin-packing-heuristic/example/bench1.pdf)

For binpacking.py to work, you need an input file containing a list of items. The example 
included in the example folder contains 500 items. The first line indicates the max. weight
and height of a bin, and then each line after that is a weight and height for a given item.
The items.py file creates item objects from an Item class, and the constraints.py file
checks to make sure a given packing does not violate the constraints.
