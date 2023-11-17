# LAB_02 

The following solution was developed together with [Andrea Pellegrino](https://github.com/andry2327/Computational-Intelligence).

Firstly we tried a few strategies, but we quickly realised that they weren't evolutionary strategies. These are `Ev_strat_1()`, `approximate_es`, `approximate_es_boosted`, which can still be tested in the notebook.
We leave them here since at least they provide good results at playing Nim.

The only evolutionary strategy implemented here is the `real_es`.
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

Basically we iterate through the rows of Nim and add to the list all the possible actions that we can make in each row. So the resulting list will be organized in the following way: [(1,1), (2,1), (2,2), ...]

The mutation takes into consideration this "ordered" structure and starting from the best parent, we generate the offsprings by mutating the index of the best parent according to a gaussian parameter ($\sim N(0,\,sigma)$). 
So given a parent move (5,1) we may generate an offspring (E.G.(5,3) , (4,3)), based on the gaussian stardard deviation (sigma).

We generate 10 different offsprings at each generation.

## Survival selection
Based on the fitness, we select the best move, between the 10 new offsprings and their generating parent.

## Fitness
To evaluate a move, we create a certain number of copies of the nim state and we employ a pure random strategy against another strategy. Our pure random strategy always starts with the move to evaluate. 
The fitness value assigned to each move is the number of wins that the pure random strategy achieve using that move as a starting one.

## Results
Based on 500 games in total, we evaluate how many games can our `real_es` strategy win against an oponent.
These are the main results:
- using `pure_random` strategy as opponent: 82 % of wins
- using `gabriele` strategy as opponent: 90 % of wins
- using `optimal` strategy as opponent: 77 % of wins

![real es VS optimal](https://github.com/andry2327/Computational-Intelligence/blob/main/LABS/L02%20-%20NIM-ES/img/plot_reals_es_VS_optimal.png)
