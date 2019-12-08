import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import ListedColormap, Normalize
import numpy as np

from search.search_dictionary import search_dictionary


def solve(arguments):

    # Parse Arguments
    dim = int(arguments['--dim'])
    wall_probability = float(arguments['--wall-probability'])
    search_type = arguments['--search']

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
        path = search_dictionary[search_type](maze, start, end)['path']
        if len(path) > 0:
            break

    fig = plt.figure()
    cmap = ListedColormap(["black", "white", "yellow"])
    norm = Normalize(vmin=0, vmax=2)
    im = plt.imshow(maze, cmap=cmap, norm=norm,
                    animated=True, interpolation='nearest')
    ax = plt.gca()
    ax.set_xticks(np.arange(-.5, dim, 1))
    ax.set_xticklabels([])
    ax.set_yticks(np.arange(-.5, dim, 1))
    ax.set_yticklabels([])

    path_grid = maze.copy()

    def update_path(coordinate):
        print(coordinate)
        path_grid[coordinate[0]][coordinate[1]] = 2
        im.set_array(path_grid)
        ax.grid(color='black', linestyle='-', linewidth=2)
        return im,

    animate = FuncAnimation(fig, update_path,
                            frames=path, blit=True, repeat=False)
    plt.show()
