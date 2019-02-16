import heapq


class Agent:
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    def __init__(self, row, column):
        self.coordinate = row, column

    def set_coordinate(self, agent_coordinate):
        self.coordinate = agent_coordinate

    def get_coordinate(self):
        return self.coordinate






