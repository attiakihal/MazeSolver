from collections import deque

# input: 2D array of bool values. True means can move there, false means cannot
# output: the shortest path. Returned as a list of coords


def bidirectional_bfs(maze, start, end):
    # Create queue
    forwards_queue = deque([[start]])
    backwards_queue = deque([[end]])
    dim = len(maze)
    visited = set()
    path = []
    forwards_curr, backwards_curr = [], []

    # Add difficulty metrics
    max_fringe = 0
    nodes_exp = 0

    while forwards_queue and backwards_queue:
        # going forwards through the maze

         # Update Max Fringe
        if len(forwards_queue) + len(backwards_queue) > max_fringe:
            max_fringe = len(forwards_queue) + len(backwards_queue)

        if forwards_queue:

            # Update Nodes Expanded
            nodes_exp = nodes_exp + 1

            forwards_curr = forwards_queue.popleft()
            # get the last row,col tuple from the path so far
            forwards_row, forwards_col = forwards_curr[-1]

            # mark the current coords as visited
            visited.add((forwards_row, forwards_col))
            # check if we ever reach the goal
            if (forwards_row == end[0] and forwards_col == end[1]) or (forwards_row, forwards_col) in backwards_queue:
                path = forwards_curr + backwards_curr[::-1]
                return {"path": path, "path_len": len(path), "max_fringe": max_fringe, "nodes_exp": nodes_exp}
            for newRow, newCol in ((forwards_row, forwards_col+1), (forwards_row+1, forwards_col), (forwards_row, forwards_col-1), (forwards_row-1, forwards_col)):
                # check if the new coords are within the bounds
                if 0 <= newRow < dim and 0 <= newCol < dim:
                    # Check if the new coords are not False, and have not been visited yet
                    if maze[newRow][newCol] == 1 and (newRow, newCol) not in visited:
                        # Add the new row,col tuple to the curr path
                        forwards_queue.append(
                            forwards_curr + [(newRow, newCol)])

        # going backwards through the maze
        if backwards_queue:

            # Update Nodes Expanded
            nodes_exp = nodes_exp + 1

            backwards_curr = backwards_queue.popleft()

            # get the last row,col tuple from the path so far
            backwards_row, backwards_col = backwards_curr[-1]

            # mark the current coords as visited
            visited.add((backwards_row, backwards_col))
            # check if we ever reach the goal
            if (backwards_row == start[0] and backwards_col == start[1]) or (backwards_col, backwards_row) in forwards_queue or (backwards_row == forwards_row and backwards_col == forwards_col):
                path = forwards_curr + backwards_curr[::-1]
                return {"path": path, "path_len": len(path), "max_fringe": max_fringe, "nodes_exp": nodes_exp}
            for newRow, newCol in ((backwards_row, backwards_col+1), (backwards_row+1, backwards_col), (backwards_row, backwards_col-1), (backwards_row-1, backwards_col)):
                # check if the new coords are within the bounds
                if 0 <= newRow < dim and 0 <= newCol < dim:
                    # Check if the new coords are not False, and have not been visited yet
                    if maze[newRow][newCol] == 1 and (newRow, newCol) not in visited:
                        # Add the new row,col tuple to the curr path
                        backwards_queue.append(
                            backwards_curr + [(newRow, newCol)])

    return {"path": [], "path_len": 0, "max_fringe": 0, "nodes_exp": 0}
