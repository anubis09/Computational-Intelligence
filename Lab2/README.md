# LAB_02 

The following solution was developed together with [Andrea Pellegrino](https://github.com/andry2327/Computational-Intelligence).

Firstly we tried a few strategies, but we quickly realised that they weren't evolutionary strategies (Other Strategies result in the notebook).
We leave them here since at least they provide good results at playing Nim.
# remember to write all not evolutionary strategy in another file, import it and then show the results.

The only evolutionary strategy implemented here is the real_es.
The idea is to generate N number of generation. For each generation:
1. Select the best parent (`tournament_selection`).
2. Mutate it to generate offsprings (`tweak`).
3. Select the best between the offsprings and the best parent. This will be one of the possible parents of the new generation (`survival_selection`).

At the end, return the best move of the last generation.

## Select the best parent 
The selection of the best parent is made with a size 5 tournament based on the fitness function. 
4 parents are chosen randomly from all the possible moves, the fifth is the best move from the last generation.

## Mutation
How do we mutate the best parent? 
At the beginning of the strategy, we create a list of all possible moves per row of Nim $\ne 0$. 

Basically we iterate through the rows of Nim and add to the list all the possible actions that we can make in that row. So the resulting list will be organized in the following way: [(1,1), (2,1), (2,2), ...]

The mutation takes into consideration this "ordered" structure and starting from the best parent, we generate the offsprings by mutating the index of the best parent according to a gaussian parameter ($\sim N(0,sigma)$). 
So given a parent move (5,1) we may generate an offspring (E.G.(5,3) , (4,3)), based on the gaussian stardard deviation (sigma).

We generate 10 different offsprings at each generation.

## Survival selection
Based on the fitness, we select the best move, between the 10 new offsprings and their generating parent.

## Fitness
To evaluate a move, we create a certain nunmber of copies of the nim state and we make play a pure random strategy against another strategy. Our pure random strategy always starts with the move to evaluate. 
The fitness value assigned to each move is the number of wins that the pure random strategy achieve using that move as a starting one.

## Results

