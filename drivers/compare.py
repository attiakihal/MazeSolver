# run all algos with differing dim size and for each dim size run it several times with different p values

import time
import subprocess
import sys
import numpy as np
from . import solve
from search.search_dictionary import search_dictionary


def compare(arguments):

    dim = int(arguments['--dim'])
    start_time = time.time()

    # run all algos with differing p sizes
    # for algo in search_dictionary:
    probs = ['.05', '0.1', '0.15', '0.2',
             '0.25', '.3', '.35', '.4', '.45', '.5']
    algos = ['dfs', 'a_star_manhattan', 'a_star_euclidean']
    for algo in algos:
        algo_start_time = time.time()
        print('running {}'.format(algo))
        p_count = 15
        for prob_str in probs:
            print('testing with p = {}'.format(prob_str))
            prob = float(prob_str)

            # Generate Grid
            # Get grid of random values
            maze = np.random.choice(a=[0,
                                       1], size=(dim, dim), p=[
                prob, 1-prob])

            # Set corner points to be unoccupied
            maze[0][0] = 1
            start = (0, 0)

            maze[dim-1][dim-1] = 1
            end = (dim-1, dim-1)

            # Run search on maze
            path = search_dictionary[algo](maze, start, end)
            print(path)
            # If maze is unsolvable, try again
            if len(path) == 0:
                while p_count > 0 and path == []:
                    path = search_dictionary[algo](maze, start, end)
                    p_count -= 1
                if path == []:
                    print(
                        'Maze unsolvable after 15 tries -- p {} is likely too high'.format(prob))
        algo_end_time = time.time()
        print('{} algo took {} time to run'.format(
            algo, algo_end_time - algo_start_time))

    global_time = time.time()
    print('Overall time was {}'.format(global_time - start_time))
    return global_time - start_time


def check_solvability(arguments):

    dim = int(arguments['--dim'])

    # run all algos with differing p sizes
    probs = ['.05', '0.1', '0.15', '0.2',
             '0.25', '.3', '.35', '.4', '.45', '.5']
    solvable = 0
    insolvable = 0
    solvable_rates = []
    algo = 'a_star_manhattan'

    for prob_str in probs:
        print('testing with p = {}'.format(prob_str))
        prob = float(prob_str)
        mazes = []

        while len(mazes) < 5:
            # Generate Grid
            # Get grid of random values
            maze = np.random.choice(a=[0,
                                       1], size=(dim, dim), p=[
                prob, 1-prob])

            # Set corner points to be unoccupied
            maze[0][0] = 1

            maze[dim-1][dim-1] = 1
            mazes.append(maze)

        end = (dim-1, dim-1)
        start = (0, 0)
        # Run search on maze
        for maze in mazes:
            path = search_dictionary[algo](maze, start, end)
            if len(path) == 0:
                insolvable += 1
            else:
                solvable += 1

            solvability = (solvable) / (solvable + insolvable)
            solvable_rates.append((solvability, prob))

        mazes = []

    file = open('/Users/kuber/GradAI/GradAI/Project1/data/solvability.txt', 'w')
    file.write(str(solvable_rates))
    file.close()
    return solvable_rates


def a_star_comparison(arguments):

    dim = int(arguments['--dim'])

    # run all algos with differing p sizes
    prob = .3

    mazes = []
    while len(mazes) < 10:
        # Generate Grid
        # Get grid of random values
        maze = np.random.choice(a=[0,
                                   1], size=(dim, dim), p=[
            prob, 1-prob])

        # Set corner points to be unoccupied
        maze[0][0] = 1

        maze[dim-1][dim-1] = 1
        mazes.append(maze)

    manhattan_times = []
    euclidean_times = []

    end = (dim-1, dim-1)
    start = (0, 0)
    # Run a* manhattan
    for maze in mazes:
        manhattan_start_time = time.time()

        manhattan_path = search_dictionary['a_star_manhattan'](
            maze, start, end)
        manhattan_end_time = time.time()
        manhattan_times.append(manhattan_end_time - manhattan_start_time)

    # Run a* euclidean
    for maze in mazes:
        euclidean_start_time = time.time()

        euclidean_path = search_dictionary['a_star_euclidean'](
            maze, start, end)
        # If maze is unsolvable, try again
        euclidean_end_time = time.time()
        euclidean_times.append(euclidean_end_time - euclidean_start_time)

    avg_manhattan_times = sum(manhattan_times) / len(manhattan_times)
    avg_euclidean_times = sum(euclidean_times) / len(euclidean_times)

    file = open(
        '/Users/kuber/GradAI/GradAI/Project1/data/a_star_comparison.txt', 'w')
    file.write("A* Manhattan times:\n")
    file.write(str(manhattan_times))
    file.write("\n")
    file.write("Average time for Manhattan:\n")
    file.write(str(avg_manhattan_times))
    file.write("A* Euclidean times:\n")
    file.write(str(euclidean_times))
    file.write("\n")
    file.write("Average time for Euclidean:\n")
    file.write(str(avg_euclidean_times))
    file.close()
    return manhattan_times, euclidean_times


def compare_shortest_path(arguments):
    probs = ['.05', '.1', '.15', '.2', '.25', '.3']
    dim = int(arguments['--dim'])
    algo = 'a_star_manhattan'

    path_lengths = []

    for prob_str in probs:
        print('Running with p = {}'.format(prob_str))
        prob = float(prob_str)
        mazes = []

        while len(mazes) < 5:
            # Generate Grid
            # Get grid of random values
            maze = np.random.choice(a=[0,
                                       1], size=(dim, dim), p=[
                prob, 1-prob])

            # Set corner points to be unoccupied
            maze[0][0] = 1
            maze[dim-1][dim-1] = 1
            mazes.append(maze)

        end = (dim-1, dim-1)
        start = (0, 0)
        # Run search on maze
        # for maze in mazes:
        maze = mazes[0]
        path = search_dictionary[algo](maze, start, end)
        # If maze is unsolvable, try again
        if len(path) == 0:
            while len(path) == 0:
                #print('not solvable, retrying...')
                # Generate new maze
                maze = np.random.choice(a=[0,
                                           1], size=(dim, dim), p=[
                                        prob, 1-prob])
                maze[0][0] = 1
                maze[dim-1][dim-1] = 1
                path = search_dictionary[algo](maze, start, end)
        path_lengths.append((len(path), prob_str))

        mazes = []
    file = open('data/shortest_paths.txt', 'w')
    file.write(str(path_lengths))
    file.close()
    return path_lengths
