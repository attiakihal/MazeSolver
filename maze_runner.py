"""Maze Runner.

Usage:
  maze_runner.py solve --dim=<n> --wall-probability=<p> --search=<search_type>
  maze_runner.py solve_fire --dim=<n> --wall-probability=<p> --search=<search_type> --fire-probability=<q> [--improved]
  maze_runner.py compare_fire
  maze_runner.py maze_gen --dim=<n> --wall-probability=<p> --search=<search_type> --metric=<diff_metric>
  maze_runner.py compare --dim=<n>
  maze_runner.py maze_gen --dim=<n> --wall-probability=<p> --search=<search_type> --metric=<diff_metric>
  maze_runner.py check_solvability --dim=<n>
  maze_runner.py a_star_comparison --dim=<n>
  maze_runner.py compare_shortest_path --dim=<n> 

  maze_runner.py --version

Options:
  -h --help                 Show this screen.
  -v --version                 Show version.
  -d --dim=<n>                 Array will be of shape (dim x dim).
  -s --search=<search_type>    Search algorithm to solve the maze.
  -w --wall-probability=<p>    Probability that a block will be a wall.
  -f --fire-probability=<q>    Probability that a fire will spread to an adjacent block.
  -i --improved                Whether you use the smart algorithm to combat fire
  -m --metric=<diff_metric>    The metric used to calculate how difficult a certain maze is. Choose from: path_len, max_fringe, nodes_exp

"""

# Import Required Libraries
from docopt import docopt

# Import Drivers
from drivers.solve import solve
from drivers.solve_fire import solve_fire
from drivers.solve_fire import compare_fire
from drivers.compare import compare
from drivers.maze_gen import maze_gen
from drivers.compare import check_solvability
from drivers.compare import a_star_comparison
from drivers.compare import compare_shortest_path


if __name__ == '__main__':

    # Get argument values
    arguments = docopt(__doc__, version='Maze Runner 1.0')

    if arguments['solve']:
        solve(arguments)
    elif arguments['solve_fire']:
        solve_fire(arguments)
    elif arguments['solve_fire']:
        compare(arguments)
    elif arguments['maze_gen']:
        maze_gen(arguments)
    elif arguments['compare_fire']:
        compare_fire()
    elif arguments['check_solvability']:
        check_solvability(arguments)
    elif arguments['a_star_comparison']:
        a_star_comparison(arguments)
    elif arguments['compare_shortest_path']:
        compare_shortest_path(arguments)
