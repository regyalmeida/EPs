import math
import numpy
import random
import matplotlib.pyplot as plt
from numpy.random import choice, randint
from statistics import mean

##### Constants declarations #####
population_size = 500

max_generations = 200

selected_for_competition = int((population_size * 30)/100)
selected_competition_index = []

crossover_mask = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

# roulette_wheel || k_way_tournament
selection_algorithm = 'k_way_tournament'

cloning_rate = 0        # not used
crossover_rate = 0.7
mutation_rate = 0.01


# Generates a random population with a value of 0 or 1 on each subject gene, with a probability of 0.5 for each
def population_inicialization(population_size):
    population = []
    for i in range(population_size):
        line = []
        for j in range(20):
            gene = generate_random_subject(j)
            line.append(gene)
        population.append(line)

    # population = [[0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0],
    #               [0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    #               [1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1],
    #               [1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0],
    #               [1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0]]
    return population


# Generates a random subject with a value of 0 or 1, with a probability of 0.5 for each
def generate_random_subject(index):
    candidates_mask = [0, 1]
    for i in range(20):
        if(i == index):
            # choice(list_of_candidates, number_of_items_to_pick, p=probability_distribution)
            gene = choice(candidates_mask, 1, 0.5)

    return gene[0]


# Recieve a population and return its values of fitness, rastrings and odds of choice for each subject
def apply_population_fitness(population):
    population_odds = []
    population_fitness = []
    population_rastrings = []

    for i in range(population_size):
        fitness, rastrigins = define_subject_fitness(population[i])
        population_rastrings.append(rastrigins)
        population_fitness.append(fitness)

    for ind_fitness in population_fitness:
        population_odds.append((ind_fitness / sum(population_fitness)))

    return population_fitness, population_rastrings, population_odds


# Recieve a subject and return its values of fitness and rastrings
# for this, split x,y bits, convert it to decimal number and apply the formula
def define_subject_fitness(subject):

    bin_x = subject[0:10]
    bin_y = subject[10:20]

    dec_x = bin_2_dec(bin_x)
    dec_y = bin_2_dec(bin_y)

    fitness = 0
    rastrigins_result = rastrigins(dec_x, dec_y)
    fitness = 100 - rastrigins_result

    return (fitness, rastrigins_result)


# Recieves a binary in an array and returns its respective number in decimal
def bin_2_dec(bin_number):
    string_number = "0b"
    length = len(bin_number)

    for i in range(length):
        string_number += str(bin_number[i])

    dec_number = int(string_number, base=0)
    float_number = float(dec_number)
    number = ((float_number) * 0.00978) - 5

    return number


# Rastrigins Function with 2 dimensions
def rastrigins(x, y):
    powX = math.pow(x, 2)
    powY = math.pow(y, 2)
    cosX = math.cos(2 * math.pi * x)
    cosY = math.cos(2 * math.pi * y)

    result = 20 + powX + powY - 10*(cosX + cosY)
    return result


# Get DA BEST generation subject with its respective values
def get_badass_subject(population, population_rastrings, population_fitness):
    best_result = min(population_rastrings)
    best_fitness = population_fitness[population_rastrings.index(best_result)]
    badass_subject = population[population_rastrings.index(best_result)]
    return badass_subject, best_result, best_fitness


def get_data_graphic(population, population_rastrings, population_fitness):
    best_result = min(population_rastrings)
    best_fitness = population_fitness[population_rastrings.index(best_result)]
    badass_subject = population[population_rastrings.index(best_result)]

    fitness_mean = mean(population_fitness)
    return badass_subject, best_result, best_fitness, fitness_mean


# Recieve a population and each subject odds of choice and return a new generation
# uses a selection algorithm, crossover and mutation
def create_new_generation(population, population_odds, population_fitness, population_rastrings):
    new_generation = []

    while len(new_generation) < len(population):

        x = selection(population, population_odds,
                      population_fitness, population_rastrings)
        y = selection(population, population_odds,
                      population_fitness, population_rastrings)

        # Crossover part
        crossover_chance = random.uniform(0, 1)
        if(crossover_chance <= crossover_rate):
            child_1, child_2 = crossover(x, y)
        else:
            child_1, child_2 = cloning(x, y)

        new_subject_1 = string_2_array(child_1)
        new_subject_2 = string_2_array(child_2)

        # Mutation part
        for i in range(2):
            mutation_chance = random.uniform(0.001, 0.01)
            if(mutation_chance <= mutation_rate):
                if (i == 0):
                    new_subject_1 = mutation(new_subject_1)
                elif (i == 1):
                    new_subject_2 = mutation(new_subject_2)

        new_generation.append(new_subject_1)
        new_generation.append(new_subject_2)
        if len(new_generation) == len(population):
            break

    return new_generation


def selection(population, population_odds, population_fitness, population_rastrings):
    chosen_one = ""

    if selection_algorithm == 'roulette_wheel':
        chosen_one = roulette_wheel_selection(
            population, population_odds)
    elif selection_algorithm == 'k_way_tournament':
        chosen_one = k_way_tournament(
            population, population_odds, population_fitness)

    return chosen_one


def roulette_wheel_selection(population, population_odds):
    odds = 0
    roulette = []
    chosen_one = 0
    candidates_mask = range(0, 1)

    for odd in population_odds:
        odds += odd
        roulette.append(odds)

    spin_number = random.uniform(0, 1)
    position = 0

    for roulette_slice in range(len(roulette)):
        if(spin_number <= roulette[roulette_slice]):
            chosen_one = position
            break
        position += 1

    return population[chosen_one]


def k_way_tournament(population, population_odds, population_fitness):

    selected_subjects = []
    selected_subjects_fitness = []
    for i in range(population_size):
        selected_subjects.append(-1000)
        selected_subjects_fitness.append(-1000)

    selected_for_competition_index = selected_competition_index
    selected_index = []

    # for i in range(selected_for_competition):
    #     subject_position = choice(choice_mask, 1)
    #     selected_subjects.append(population[subject_position[0]])
    #     selected_subjects_fitness.append(population_fitness[subject_position[0]])

    # range (0,1,2, 3) if selected = 4
    for i in range(selected_for_competition):
        subject_position = random.randint(0, population_size-1)
        # if (subject_position in selected_for_competition_index):
        #     subject_position = random.choice(range(0, population_size))
        # elif (not subject_position in selected_for_competition_index):

        # selected_subjects.append(population[subject_position])
        # selected_subjects_fitness.append(population_fitness[subject_position])
        # selected_for_competition_index.append(subject_position)

        selected_subjects[subject_position] = population[subject_position]
        selected_subjects_fitness[subject_position] = population_fitness[subject_position]
        selected_index.append(subject_position)

    best_fitness = max(selected_subjects_fitness)
    chosen_one = selected_subjects[selected_subjects_fitness.index(
        best_fitness)]

    # best_fitness = 0
    # best_fitness_index = 0
    # for i in range(len(selected_subjects)):
    #     if(selected_subjects_fitness[i] >= best_fitness):
    #         best_fitness = selected_subjects_fitness[i]
    #         best_fitness_index = i
    # chosen_one = selected_subjects[best_fitness_index]
    selected_for_competition_index = []
    return chosen_one


def crossover(x, y):

    child1 = []
    child2 = []

    for i in range(len(crossover_mask)):
        if crossover_mask[i] == 1:
            child2.append(x[i])
            child1.append(y[i])
        else:
            child1.append(x[i])
            child2.append(y[i])

    return child1, child2


def cloning(x, y):
    child = ""
    first_parent = ""
    second_parent = ""

    for i in range(len(x)):
        first_parent += str(x[i])
    for i in range(len(y)):
        second_parent += str(y[i])

    child_1 = first_parent
    child_2 = second_parent
    return child_1, child_2


def mutation(child):
    choice_mask = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
                   10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
    position = choice(choice_mask, 1)

    muted = False
    for i in range(len(child)):
        if(muted == False):
            if(i == position[0]):
                if(child[i] == 0):
                    child[i] = 1
                elif (child[i] == 1):
                    child[i] = 0
                muted = True
                new_child = child
        elif muted:
            break

    return new_child


def string_2_array(subject):
    new_subject = []
    for j in range(20):
        gene = int(subject[j])
        new_subject.append(gene)

    return new_subject


def generate_graphic(fitness_mean_array, best_fitness_array):
    x = 10*numpy.array(range(len(fitness_mean_array)))
    plt.plot(x, best_fitness_array, color='blue')
    plt.plot(x, fitness_mean_array, color='orange')
    plt.xlabel("Número de gerações")
    plt.xlim(0, max_generations)
    plt.legend(["Subject", "Mean"])
    plt.grid(True)
    plt.show()

    return


# Where it all begins
def main():
    population = population_inicialization(population_size)

    generations_array = []
    best_result_array = []
    best_fitness_array = []
    fitness_mean_array = []
    badass_subject_array = []

    generation = 0
    while (generation < max_generations):

        population_fitness, population_rastrings, population_odds = apply_population_fitness(
            population)

        badass_subject, best_result, best_fitness, fitness_mean = get_data_graphic(
            population, population_rastrings, population_fitness)

        best_result_array.append(best_result)
        best_fitness_array.append(best_fitness)
        fitness_mean_array.append(fitness_mean)
        badass_subject_array.append(badass_subject)
        generations_array.append(generation)

        print(best_fitness)

        # x = 10*numpy.array(range(len(population_fitness)))
        # plt.plot(x, population_fitness, color='green')
        # plt.xlim(0, max_generations)
        # plt.show()

        population = create_new_generation(
            population, population_odds, population_fitness, population_rastrings)
        generation += 1

    generate_graphic(fitness_mean_array, best_fitness_array)
main()
