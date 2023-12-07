# LAB9

The following solution was developed together with [Andrea Pellegrino](https://github.com/andry2327/Computational-Intelligence).

The evolution strategy we implemented follows these steps for each generation:
- Parent selection: with a variable tournament size (default value 3).
- Uniform crossover: we always apply crossover to two parents.
- Mutation: we apply mutation with a certain probabiity to the result of the crossover operation.
- Survival selection: select the best ```population_size``` between population and offsprings.

One can choose two different implementations of the evolution algorithm and two different mutation strategies.
The evolutionary algorithm creates generations until the optimal fitness value remains constant for a specified number of generations.

## Classic EA
This is just the implementation of the steps described above.

## Island model
We created a given number of islands where an island is a population itself. We evolve each island independently for a given number of generations (regulated by ```migration_frequency``` parameter), after that we remove a certain amount of population from each island and we migrate them to a random island. 

## Bit flip mutation
If mutation occurs, we itereate through the genotype and with a given probability (```Ea.__bit_change```), we flip the gene.

## Bit assign mutation
If mutation occurs, we choose the value (0/1) to assign based on a given probability (```Ea.__prob_to_set_1```). 
we itereate through the genotype and with a given probability (```Ea.__bit_change```), we assign the value to the gene.
The mutated individual is evaluated and if it's better than the parent, we increment a counter for the value assigned (```Ea.__better_with_0_1```). 
At the end of whole generation, ```Ea.__prob_to_set_1``` is self adjusted based on the performance of the bit assigned.

# Results

Bit flip mutation, no island model is the best one overall. The other do not show same performances. 
Across multiple runs, we notices that the bit assign strategy is not robust and results are variable.

### Bit flip mutation, no island model:
- Problem instance: 1, Best individual fitness: 1.0, Generation num: 135, Fitness calls: 27200 -> fitness/fitness_call adjusted: 367.6471
- Problem instance: 2, Best individual fitness: 1.0, Generation num: 299, Fitness calls: 60000 -> fitness/fitness_call adjusted: 166.6667
- Problem instance: 5, Best individual fitness: 0.71, Generation num: 132, Fitness calls: 26600 -> fitness/fitness_call adjusted: 266.9173
- Problem instance: 10, Best individual fitness: 0.49, Generation num: 762, Fitness calls: 152600 -> fitness/fitness_call adjusted: 31.8990

![img1](https://github.com/andry2327/Computational-Intelligence/blob/main/LABS/L09/imgs/%231%20Bit%20flip%20mutation%2C%20no%20island%20model/output1.png)

### Bit flip mutation, with island model:
- Problem instance: 1, Best individual fitness: 1.0, Generation num: 100, Fitness calls: 80200 -> fitness/fitness_call adjusted: 124.6883
- Problem instance: 2, Best individual fitness: 1.0, Generation num: 240, Fitness calls: 192200 -> fitness/fitness_call adjusted: 52.0291
- Problem instance: 5, Best individual fitness: 0.57, Generation num: 80, Fitness calls: 64200 -> fitness/fitness_call adjusted: 89.5327
- Problem instance: 10, Best individual fitness: 0.41, Generation num: 160, Fitness calls: 128200 -> fitness/fitness_call adjusted: 32.1654

![img1](https://github.com/andry2327/Computational-Intelligence/blob/main/LABS/L09/imgs/%232%20Bit%20flip%20mutation%2C%20with%20island%20model/output2.png)

### Bit assign strategy, no island model:
- Problem instance: 1, Best individual fitness: 0.952, Generation num: 213, Fitness calls: 43000 -> fitness/fitness_call adjusted: 221.3953
- Problem instance: 2, Best individual fitness: 0.856, Generation num: 1052, Fitness calls: 210800 -> fitness/fitness_call adjusted: 40.6072
- Problem instance: 5, Best individual fitness: 0.525, Generation num: 336, Fitness calls: 67600 -> fitness/fitness_call adjusted: 77.6627
- Problem instance: 10, Best individual fitness: 0.269, Generation num: 239, Fitness calls: 48200 -> fitness/fitness_call adjusted: 55.9528

![img1](https://github.com/andry2327/Computational-Intelligence/blob/main/LABS/L09/imgs/%233%20Bit%20assign%20strategy%2C%20no%20island%20model/output3.png)

### Bit assign strategy, with island model:
- Problem instance: 1, Best individual fitness: 0.912, Generation num: 180, Fitness calls: 144400 -> fitness/fitness_call adjusted: 63.1579
- Problem instance: 2, Best individual fitness: 0.486, Generation num: 80, Fitness calls: 64400 -> fitness/fitness_call adjusted: 75.4658
- Problem instance: 5, Best individual fitness: 0.4305, Generation num: 140, Fitness calls: 112400 -> fitness/fitness_call adjusted: 38.3007
- Problem instance: 10, Best individual fitness: 0.3006733, Generation num: 120, Fitness calls: 96400 -> fitness/fitness_call adjusted: 31.1902

![img1](https://github.com/andry2327/Computational-Intelligence/blob/main/LABS/L09/imgs/%234%20Bit%20assign%20strategy%2C%20with%20island%20model/output4.png)


# Peer review
[Paola Matassa](https://github.com/PaolaMts/ComputationalIntelligence/issues/4)
[Arild Strømsvåg](https://github.com/arildus/computational-intelligence](https://github.com/arildus/computational-intelligence/issues/1)https://github.com/arildus/computational-intelligence/issues/1)
