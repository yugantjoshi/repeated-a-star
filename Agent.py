import heapq


class Agent:
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    def __init__(self, row, column):
        self.coordinate = row, column
        # All cells that it encounters on the way
        self.discoveredCells = []
        # Permanent path route that is chosen so far
        self.currentPath = []
        # Projected path to take
        self.heap = []

    def set_coordinate(self, agent_coordinate):
        self.coordinate = agent_coordinate

    def get_coordinate(self):
        return self.coordinate

    def add_checked_cell(self, cell_coordinate):
        self.discoveredCells.insert(0, cell_coordinate)

    def add_to_current_path(self, cell_coordinate):
        self.currentPath.insert(0, cell_coordinate)

    def get_checked_cells(self):
        return self.discoveredCells

    def get_current_path(self):
        return self.currentPath






