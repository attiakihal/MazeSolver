import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import ListedColormap, Normalize
import numpy as np
from copy import deepcopy
import random

from search.search_dictionary import search_dictionary

# Check if the diagonal from top left to bot right exists
# Check if the diagoonal from top right to bot left exists
# Do this by running A* from the corners?
def check_diagonals(maze):
    return len( search_dictionary['a_star_manhattan']( maze, (0, len(maze)-1), (len(maze)-1, 0) )['path'] ) > 0

# return final path of the algo
# return list of sets of coords of fires
def fire_driver(maze, search_type, q, start, end, smart):

    # run algo to find path
    path = search_dictionary[search_type](maze, start, end)['path']

    # not starting at 0 because that should just be the "start" coord
    counter = 1

    # list of coords of the final traversed path
    final_path = [(0, 0)]
    # list of sets of the fire
    final_fire = [set([(0, len(maze)-1)])]

    # return val
    final = {}

    # loop through each step of shortest
    while maze[end[0]][end[1]] != 2:
        # get cell trying to move into
        row, col = path[counter]
        # check if the curr coord we are changing to is not on fire
        if maze[row][col] != 3:
            # update map to show coordinate of curr path locaiton
            maze[row][col] = 2
        elif smart:
            # the cell we want to go to was on fire
            # check if we are using the improved algorithm
            print(f"Can't Move to {(row,col)}! Finding New Path")
            # Re run algo from cell prior (the one we are trying to move FROM)
            if counter != 0:
                start = path[counter-1]
            else:
                start = path[counter]

            path = search_dictionary[search_type](maze, start, end)['path']

            # if there is a path
            if path:
                # take first step of that path
                row, col = path[1]
                maze[row][col] = 2
                counter = 1
            else:
                # if not, return path and stuff I have currently because there is no path anymore (fire blocks all paths)
                final.update({'path': final_path})
                final.update({'fire': final_fire})
                return final
        else:
            # Fire is in the way so return because fire is going to kill since it cannot move into fire
            final.update({'path': final_path})
            final.update({'fire': final_fire})
            return final

        # add the curr step that we just took to the path
        final_path.append((row, col))

        # run the fire spread, if lands on person then die
        curr_fire = update_fire(maze, q)

        # Check if any fire spread
        if len(curr_fire) == 0:
            curr_fire = None
        else:
            # Change the cells to fire cells
            for fire_coord in curr_fire:
                maze[fire_coord[0]][fire_coord[1]] = 3
        # add the curr set of the fire to the final list
        final_fire.append(curr_fire)

        # check to see if you die
        if curr_fire is not None:
            if (row, col) in curr_fire:
                print(f"Crashed at {(row, col)}")
                final.update({'path': final_path})
                final.update({'fire': final_fire})
                return final

        # increment counter
        counter += 1

    # we have reached the end of the maze. Return what we have
    final.update({'path': final_path})
    final.update({'fire': final_fire})
    return final

# Compares the improved algorithm to the basic algorithm through the list of q values
# Test on a 100x100 map
def compare_fire():

    # q values testing
    q_values = [0, .05, .1, .15, .2, .25, .3, .35, .4, .45, .5, .55, .6, .65, .7, .75, .8, .85, .9, .95, 1]

    start = (0,0)
    dim = 100
    end = (dim-1,dim-1)
    search_type = 'a_star_manhattan'
    # wall probaility we found (p0)
    wall_probability = .3

    # Run until we get a solvable maze
    while True:
        # Get grid of random values
        maze = np.random.choice(a=[0,
                                   1], size=(dim, dim), p=[
            wall_probability, 1-wall_probability])

        # Set corner points to be unoccupied
        maze[0][0] = 1
        start = (0, 0)

        maze[dim-1][dim-1] = 1
        end = (dim-1, dim-1)

        # Step top right corner on fire
        maze[0][dim-1] = 3

        # Create copy of maze to run algo
        path_grid = deepcopy(maze)
        diagonal_grid = deepcopy(maze)
        path = search_dictionary["a_star_manhattan"](path_grid, start, end)['path']
        # Check if there is a solution and if there are diagonals open
        if (path or len(path) != 0) and (check_diagonals(diagonal_grid)):
            break
        print('Generate new Map')

    # create the file
    f = open("fire_data.txt","w+")

    # Solve for all q values
    for q in q_values:
        maze_copy = deepcopy(maze)
        second_copy = deepcopy(maze)
        # Run with basic algo
        final = fire_driver(maze_copy, search_type, q, start, end, False)
        # Run with improved algo
        finalSmart = fire_driver(second_copy, search_type, q, start, end, True)
        if end in final['path']:
            # it got to the end
            f.write("({}, dumb, successful), ".format(q))
        else:
            # it died
            f.write("({}, dumb, fails), ".format(q))
        if end in finalSmart['path']:
            # It got to the end
            f.write("({}, smart, successful), ".format(q))
        else:
            # It died
            f.write("({}, smart, fails), ".format(q))

    f.close()

# Solve the maze while fire spreads
def solve_fire(arguments):
    # Parse Arguments
    dim = int(arguments['--dim'])
    wall_probability = float(arguments['--wall-probability'])
    search_type = arguments['--search']
    q = float(arguments['--fire-probability'])
    smart = arguments['--improved']

    while True:
        # Get grid of random values
        maze = np.random.choice(a=[0,
                                   1], size=(dim, dim), p=[
            wall_probability, 1-wall_probability])

        # Set corner points to be unoccupied
        maze[0][0] = 1
        start = (0, 0)

        maze[dim-1][dim-1] = 1
        end = (dim-1, dim-1)

        # set top right cell on fire
        maze[0][dim-1] = 3

        path_grid = deepcopy(maze)
        diagonal_grid = deepcopy(maze)
        path = search_dictionary["a_star_manhattan"](path_grid, start, end)['path']
        if (path or len(path) != 0) and (check_diagonals(diagonal_grid)):
            break
        print('Generate new Map')

    final = fire_driver(maze, search_type, q, start, end, smart)
    # zip the path and the sets of fire to plot
    mapped = zip(final['path'], final['fire'])
    dim = len(maze)

    fig = plt.figure()
    cmap = ListedColormap(["black", "white", "yellow", "red"])
    norm = Normalize(vmin=0, vmax=3)
    im = plt.imshow(path_grid, cmap=cmap, norm=norm,
                    animated=True, interpolation='nearest')
    ax = plt.gca()
    ax.set_xticks(np.arange(-.5, dim, 1))
    ax.set_xticklabels([])
    ax.set_yticks(np.arange(-.5, dim, 1))
    ax.set_yticklabels([])

    def update_path(coordinate_and_fire):
        print(coordinate_and_fire)
        path_coordinate, fire_coordinates = coordinate_and_fire
        path_grid[path_coordinate[0]][path_coordinate[1]] = 2
        if fire_coordinates:
            for fire_coordinate in fire_coordinates:
                print(fire_coordinate)
                path_grid[fire_coordinate[0]][fire_coordinate[1]] = 3

        im.set_array(path_grid)
        ax.grid(color='black', linestyle='-', linewidth=2)
        return im,

    FuncAnimation(fig, update_path,
                  frames=mapped, blit=True, repeat=False)
    plt.show()

# Find out which coords are going to catch on fire and then return the set of all coords that catch on fire
def update_fire(map, q):
    # store coords of the new fire we are adding
    newFire = set()

    # we are going to traverse through the whole entire map finding fire and updating
    dim = len(map)
    for row in range(dim):
        for col in range(dim):
            neighbor_fire = 0
            # check if the current coord is either an empty path or a visited one
            if map[row][col] == 1 or map[row][col] == 2:
                # check around this current spot for the number of those on fire
                for newRow, newCol in ((row, col+1), (row+1, col), (row, col-1), (row-1, col)):
                    # check if the new coords are within the bounds
                    if (0 <= newRow < dim) and (0 <= newCol < dim):
                        if map[newRow][newCol] == 3:
                            # increase the number of neigbors that are on fire
                            neighbor_fire += 1
                # calculate if cell catches on fire
                if random.random() < (1 - (1 - q)**neighbor_fire):
                    newFire.add((row, col))

    return newFire
