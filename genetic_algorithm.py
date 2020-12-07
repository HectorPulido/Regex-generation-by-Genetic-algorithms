import random


class GeneticAlgorithm:
    def __init__(
        self,
        population_size,
        elitism,
        new_population,
        string_length,
        mutation_rate,
        simbols,
        score_func,
    ):
        self.population_size = population_size
        self.elitism = elitism
        self.new_population = new_population
        self.string_length = string_length
        self.mutation_rate = mutation_rate
        self.score_func = score_func
        self.simbols = simbols

    def calculate_population_score(self, population):
        return [self.score_func(individual) for individual in population]

    def set_selection(self):
        populaton_weights = [i for i in range(self.population_size)]
        populaton_weights.reverse()

        return random.choices(
            self.population, weights=populaton_weights, k=self.population_size
        )

    def set_crossover(self):
        new_population = []
        for _ in range(self.crossover_size):
            parent_1 = random.choice(self.population)
            parent_2 = random.choice(self.population)

            new_individual = [
                parent_1[i] if random.random() > 0.5 else parent_2[i]
                for i in range(self.string_length)
            ]

            new_individual = "".join(new_individual)
            new_population.append(new_individual)

        return new_population

    def replace_str_index(self, text, index=0, replacement=""):
        return "%s%s%s" % (text[:index], replacement, text[index + 1 :])

    def set_mutations(self):
        for individual in range(len(self.population)):
            for gene in range(self.string_length):
                if random.random() < self.mutation_rate:
                    self.population[individual] = self.replace_str_index(
                        self.population[individual],
                        index=gene,
                        replacement=random.choice(self.simbols),
                    )

        return self.population

    def set_elitism(self, population_with_score):
        elite = population_with_score[: self.elitism]
        elite_individual = [individual[0] for individual in elite]
        return self.population + elite_individual

    def generate_random_string(self):
        string = [random.choice(self.simbols) for _ in range(self.string_length)]
        return "".join(string)

    def new_individuals(self):
        new = [self.generate_random_string() for _ in range(self.new_population)]
        return self.population + new

    def sort_population(self):
        population_score = self.calculate_population_score(self.population)
        population_with_score = list(zip(self.population, population_score))
        population_with_score.sort(key=lambda val: val[1], reverse=True)
        return population_with_score

    def step(self, i):
        population_with_score = self.sort_population()

        if self.verbose and (i + 1) % self.verbose_period == 0:
            print(
                f"Iteration: {i}, Max score {population_with_score[0][1]}, Solution {population_with_score[0][0]}"
            )

        if self.threshold and population_with_score[0][1] >= self.threshold:
            self.solution = population_with_score[0][0]
            return

        self.population = [individual[0] for individual in population_with_score]
        self.population = self.set_selection()
        self.population = self.set_crossover()
        self.population = self.set_mutations()
        self.population = self.new_individuals()
        self.population = self.set_elitism(population_with_score)

    def run(self, steps=None, threshold=None, verbose=None, verbose_period=100):
        assert steps or threshold, "Threshold and steps can not be None at same time"

        self.solution = None
        self.crossover_size = self.population_size - self.new_population - self.elitism
        self.threshold = threshold
        self.verbose = verbose
        self.verbose_period = verbose_period

        self.population = [
            self.generate_random_string() for _ in range(self.population_size)
        ]

        if steps:
            for i in range(steps):
                self.step(i)
                if self.solution:
                    return self.solution
            population_with_score = self.sort_population()
            return population_with_score[0][0]

        i = 0
        while True:
            self.step(i)
            i += 1
            if self.solution:
                return self.solution
