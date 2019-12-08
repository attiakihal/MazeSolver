from search.search_dictionary import search_dictionary
import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import ListedColormap, Normalize
import numpy as np
import random
from copy import deepcopy


def maze_gen(arguments):
    """Generates hard mazes"""

    # Parse Arguments
    dim = int(arguments['--dim'])
    search_type = arguments['--search']
    diff_metric = arguments['--metric']
    wall_probability = float(arguments["--wall-probability"])

    # Get a solvable maze
    while True:
        maze = np.random.choice(a=[0,
                                   1], size=(dim, dim), p=[
            wall_probability, 1-wall_probability])
        if isSolvable(maze, (0, 0), (dim-1, dim-1)):
            break

    # Set corner points to be unoccupied
    maze[0][0] = 1
    start = (0, 0)

    maze[dim-1][dim-1] = 1
    end = (dim-1, dim-1)

    # This is the maze states array that shows how our mazes evolve over time
    maze_states = []

    # This is a list of all the possible wall locations in the maze
    possible_wall_locations = [(x, y) for x in range(dim) for y in range(dim)]

    # Generate maze states until termination condition
    t = 1.0
    while len(possible_wall_locations) > 0:

        maze_states.append(maze)
        temperature = 1.0/t
        neighbor_maze = generateNeighborMazeState(
            maze, start, end, possible_wall_locations)

        if mazeDifficulty(neighbor_maze, start, end, search_type, diff_metric) > mazeDifficulty(maze, start, end, search_type, diff_metric):
            maze = list(neighbor_maze)
        else:
            if np.random.random() <= P(maze, neighbor_maze, temperature, start, end, search_type, diff_metric):
                maze = list(neighbor_maze)
        t = t+1.0

    drawMazeStates(maze_states)


def P(maze, neighbor_maze, temperature, start, end, search_type, diff_metric):
    """This function calculates a probability based on maze difficulty and temperature"""
    return math.exp(-(mazeDifficulty(maze, start, end, search_type, diff_metric) - mazeDifficulty(neighbor_maze, start, end, search_type, diff_metric))/temperature)


def mazeDifficulty(maze, start, end, search_type, diff_metric):
    """This function calculates maze difficulty given a search type and a difficulty metric"""
    if diff_metric == "path_len":
        difficulty = search_dictionary[search_type](maze, start, end)[
            'path_len']
        return difficulty
    elif diff_metric == "max_fringe":
        difficulty = search_dictionary[search_type](maze, start, end)[
            'max_fringe']
        return difficulty
    elif diff_metric == "nodes_exp":
        difficulty = search_dictionary[search_type](maze, start, end)[
            'nodes_exp']
        return difficulty
    elif diff_metric == "sum":
        difficulty = search_dictionary[search_type](maze, start, end)['nodes_exp'] + search_dictionary[search_type](
            maze, start, end)['max_fringe'] + search_dictionary[search_type](maze, start, end)['path_len']
        return difficulty


def generateNeighborMazeState(maze, start, end, possible_wall_locations):
    """This function takes a maze and generates a neighbor maze. It will randomly generate a new wall to place.
        Note: Only valid mazes are considered to be neighbors, and walls can not be randomly generated over existing walls"""
    while True:
        neighbor_maze = deepcopy(maze)

        # If there are no more valid locations to put a wall, maze has no more neighbor states
        if len(possible_wall_locations) == 0:
            return maze

        new_wall = possible_wall_locations.pop(
            random.randrange(len(possible_wall_locations)))

        while (new_wall == (0, 0) or new_wall == (len(maze)-1, len(maze)-1) or maze[new_wall[0]][new_wall[1]] == 0):
            if len(possible_wall_locations) == 0:
                return maze
            else:
                new_wall = possible_wall_locations.pop(
                    random.randrange(len(possible_wall_locations)))

        neighbor_maze[new_wall[0]][new_wall[1]] = 0

        if isSolvable(neighbor_maze, start, end):
            return neighbor_maze


def isSolvable(maze, start, end):
    """Check if maze is solvable"""
    path = search_dictionary["a_star_manhattan"](maze, start, end)['path']
    return len(path) > 0


def drawMazeStates(maze_states):
    """Draws the evolution of the maze"""
    dim = len(maze_states[0])
    fig = plt.figure()
    cmap = ListedColormap(["black", "white", "yellow"])
    norm = Normalize(vmin=0, vmax=2)
    im = plt.imshow(maze_states[0], cmap=cmap, norm=norm,
                    animated=True, interpolation='nearest')
    ax = plt.gca()
    ax.set_xticks(np.arange(-.5, dim, 1))
    ax.set_xticklabels([])
    ax.set_yticks(np.arange(-.5, dim, 1))
    ax.set_yticklabels([])

    def update_path(maze_state):
        im.set_array(maze_state)
        ax.grid(color='black', linestyle='-', linewidth=2)
        return im,

    animate = FuncAnimation(fig, update_path,
                            frames=maze_states, blit=True, repeat=False, interval=1)
    plt.show()
