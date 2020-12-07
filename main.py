from genetic_algorithm import GeneticAlgorithm
from helpers import generate_regex_score_function, read_from_file

# Hyperparameters
population_size = 100
elitism = 5
new_population = 10
string_length = 12
steps = 1000000
threshold = 1
mutation_rate = 0.25

# Read examples
filename_positive = "examples_positive.txt"
filename_negative = "examples_negative.txt"

examples_positive = read_from_file(filename_positive)
examples_negative = read_from_file(filename_negative)

# shrink the search space
unique_characters = "".join(
    set("".join(examples_positive) + "".join(examples_negative))
)

chars = unique_characters

for char in "123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM":
    chars = chars.replace(char, "")

chars = r"ª.*+\\[]()" + chars

if any(unique_characters in s for s in list("123456789")):
    chars += r"\d"

if any(
    unique_characters in s
    for s in list("qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM")
):
    chars += r"\w"

# Genetic Algorithm
score_func = generate_regex_score_function(examples_positive, examples_negative)

genetic_algorithm = GeneticAlgorithm(
    population_size,
    elitism,
    new_population,
    string_length,
    mutation_rate,
    chars,
    score_func,
)

genetic_algorithm.run(threshold=threshold, verbose=True, verbose_period=50)
