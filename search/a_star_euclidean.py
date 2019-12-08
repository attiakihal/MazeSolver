import heapq
import math

from common.nodes import Node


def a_star_euclidean(maze, start, end):

    # Create start and end nodes
    start = Node(None, start)
    end = Node(None, end)

    # Create fringe
    fringe = []
    heapq.heapify(fringe)
    visited = list()

    # Add start node
    heapq.heappush(fringe, start)

    # Add difficulty metrics
    max_fringe = 0
    nodes_exp = 0

    while len(fringe) > 0:

        # Update Max Fringe
        if len(fringe) > max_fringe:
            max_fringe = len(fringe)

        # Update Nodes Expanded
        nodes_exp = nodes_exp + 1

        current = heapq.heappop(fringe)
        visited.append(current)

        # Found the end node
        if current == end:
            path = []
            while current is not None:
                path.append(current.position)
                current = current.parent

            # Reverse the path and return
            path = path[::-1]
            return {"path": path, "path_len": len(path), "max_fringe": max_fringe, "nodes_exp": nodes_exp}

        # Get neighbors
        neighbors = []
        for x_change, y_change in [(1, 0), (-1, 0), (0, 1), (0, -1)]:

            # Calculate position of neighbor
            x_new, y_new = (
                current.position[0] + x_change, current.position[1] + y_change)

            # Make sure neighbor is inside maze
            if x_new > (len(maze) - 1) or x_new < 0 or y_new > (len(maze) - 1) or y_new < 0:
                continue

            # Make sure neighbor is walkable
            if maze[x_new][y_new] != 1:
                continue

            # Create new node and append to neighbors
            new_node = Node(current, (x_new, y_new))
            neighbors.append(new_node)

        # Loop through neighbors
        for neighbor in neighbors:

            # Check to make sure neighbor has not already been visited
            if neighbor in visited:
                continue

            # Increase cost by one
            neighbor.cost = current.cost + 1

            # Calculate heuristic
            neighbor.heuristic = math.sqrt(
                ((neighbor.position[0] - current.position[0])**2) + ((neighbor.position[1] - current.position[1])**2))

            # Calculate total cost
            neighbor.total_cost = neighbor.cost + neighbor.heuristic

            # Check if neighbor is already in the fringe and take the smallest value
            shortest_path_to_neighbor = True
            for node in fringe:

                # If a path to the neighbor is already in the fringe
                if neighbor == node:

                    # If the path to this node is longer than one already in the fringe
                    if neighbor.total_cost >= node.total_cost:
                        shortest_path_to_neighbor = False

            if shortest_path_to_neighbor:
                heapq.heappush(fringe, neighbor)

    return {"path": [], "path_len": 0, "max_fringe": 0, "nodes_exp": 0}
