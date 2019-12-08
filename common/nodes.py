class Node():

    def __init__(self, parent, position):

        self.parent = parent
        self.position = position

        self.cost = 0
        self.heuristic = 0
        self.total_cost = 0

    def __eq__(self, other):
        return self.position == other.position

    def __lt__(self, other):
        return self.total_cost < other.total_cost

    def __gt__(self, other):
        return self.total_cost > other.total_cost

    def __hash__(self):
        return hash(self.position)
