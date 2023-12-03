POPULATION_SIZE = 1000
OFFSPRING_SIZE = 200
MUTATION_PROB = 0.2
TOURNAMENT_SIZE = 5

LOCI = 1000


class Individual:
    def __init__(self):
        self.genotype = choices([0, 1], k=LOCI)
        self.fitness = float("-inf")


def create_population(pop_size):
    population = [Individual() for _ in range(pop_size)]
    for p in population:
        p.fitness = fitness(p.genotype)
    return population


def parent_selection(
    population: list[Individual], tournament_size: int
) -> Individual:
    # we also want to take the last best one.
    parents_idx = np.random.choice(
        range(len(population)), size=tournament_size, replace=False
    )
    parents = [population[idx] for idx in parents_idx]
    return max(parents, key=lambda i: i.fitness)


def uniform_cut_xover(ind1: Individual, ind2: Individual) -> Individual:
    assert len(ind1.genotype) == len(ind2.genotype)
    p1 = ind1.fitness / (ind1.fitness + ind2.fitness)
    mask = np.random.choice([True, False], size=LOCI, p=[p1, 1 - p1])
    gene = np.where(mask, ind1.genotype, ind2.genotype)
    new_ind = Individual()
    new_ind.genotype = gene.tolist()
    return new_ind


class new_generation:
    def __init__(
        self,
        mutation_prob: float,
        bit_to_1: float = 0.5,
        bit_change: float = 0.15,
    ):
        self.mutation_prob = mutation_prob
        self.prob_to_set_1 = bit_to_1
        self.bit_change = bit_change
        self.better_with_0_1 = [0, 0]

    def mutate(self, parent):
        if random() < self.mutation_prob:
            new_offspring = deepcopy(parent)
            bit_val = 1 if random() < self.prob_to_set_1 else 0
            for i in range(len(parent.genotype)):
                if random() < self.bit_change:
                    new_offspring.genotype[i] = bit_val
            new_offspring.fitness = fitness(new_offspring.genotype)
            if new_offspring.fitness > parent.fitness:
                self.better_with_0_1[bit_val] += 1
            return new_offspring
        else:
            # no mutate, just fitness calculation
            parent.fitness = fitness(parent.genotype)
            return parent

    def adjust_prob(self):
        if self.better_with_0_1[1] > self.better_with_0_1[0]:
            self.prob_to_set_1 += 0.1
        else:
            self.prob_to_set_1 -= 0.1
        self.better_with_0_1 = [0, 0]

    def __call__(
        self, population: list[Individual], offspring_size, tournament_size
    ) -> list[Individual]:
        offsprings = []
        for _ in range(offspring_size):
            parent1 = parent_selection(population, tournament_size)
            parent2 = parent_selection(population, tournament_size)
            offspring = uniform_cut_xover(parent1, parent2)
            offspring = self.mutate(offspring)
            offsprings.append(offspring)
        self.adjust_prob()
        return offsprings


instance = [10]
for k in instance:
    fitness = lab9_lib.make_problem(k)
    evolution_algorithm = Ea(fitness)
    best_individual = evolution_algorithm()
    best_fitness = best_individual.fitness
    print(
        f"\nBest individual fitness: {best_fitness}, Fitness calls: {fitness.calls} -> Score2: {best_fitness/fitness.calls*10000000:.4f}"
    )
