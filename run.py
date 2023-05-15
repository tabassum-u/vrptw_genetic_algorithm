# https://github.com/radoslawik/VRPTW_GA_PSO

from genetic import *
from numpy import random

if __name__ == '__main__':

    random.seed(231)
    plot_result = True
    problem_name = 'C101'
    alg_name = 'Genetic Algorithm'

    customers_count = 100
    max_generations = 100

    population_size = 100
    crossover_prob = 0.9
    mutation_prob = 0.09

    print('### GENERAL INFO ###')
    print('Problem name: ' + problem_name)
    print(f'Customer count: {customers_count}')
    print(f'Max iterations: {max_generations}')
    print('Algorithm: ' + alg_name)
    print('### ALGORITHM PARAMETERS ###')

    res = run_ga(instance_name=problem_name, individual_size=customers_count, pop_size=population_size,
                 cx_pb=crossover_prob, mut_pb=mutation_prob, n_gen=max_generations, plot=plot_result
                 )


