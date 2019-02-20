import heapq


class Agent:

    def __init__(self, row, column):
        self.row = row
        self.column = column
        self.coordinate = row, column

    def set_coordinate(self, agent_coordinate):
        self.coordinate = agent_coordinate

    def set_row(self, row):
        self.row = row

    def set_column(self, column):
        self.column = column

    def get_coordinate(self):
        return self.coordinate

    def get_row(self):
        return self.row

    def get_column(self):
        return self.column






