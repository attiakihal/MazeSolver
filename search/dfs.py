from collections import deque


# input: 2D array of bool values. True means can move there, false means cannot
# output: the shortest path. Returned as a list of coords


def dfs(maze, start, end):

    # Create stack
    stack = deque([[start]])
    dim = len(maze)
    visited = set()

    # mark the starting coords as visited
    visited.add(start)

    # Add difficulty metrics
    max_fringe = 0
    nodes_exp = 0

    while stack:

        # Update Max Fringe
        if len(stack) > max_fringe:
            max_fringe = len(stack)

        # Update Nodes Expanded
        nodes_exp = nodes_exp + 1

        curr = stack.pop()

        # get the last row,col tuple from the path so far
        row = curr[-1][0]
        col = curr[-1][1]

        # mark the current coords as visited
        visited.add((row, col))

        # check if we ever reach the goal
        if row == end[0] and col == end[1]:
            return {"path": curr, "path_len": len(curr), "max_fringe": max_fringe, "nodes_exp": nodes_exp}

        for newRow, newCol in [(row+1, col), (row, col-1), (row-1, col), (row, col+1)]:
            # check if the new coords are within the bounds
            if 0 <= newRow < dim and 0 <= newCol < dim:
                # Check if the new coords are not False, and have not been visited yet
                if maze[newRow][newCol] == 1 and (newRow, newCol) not in visited:
                    # Add the new row,col tuple to the curr path
                    stack.append(curr + [(newRow, newCol)])
                    visited.add((newRow, newCol))

    return {"path": [], "path_len": 0, "max_fringe": 0, "nodes_exp": 0}
