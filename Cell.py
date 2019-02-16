class Cell:

    def __init__(self, row, column):
        self.row = row
        self.column = column
        self.isBlocked = False
        self.g_value = -1
        self.h_value = -1
        self.f_value = -1

    def set_g_value(self, agent_initial_coordinate):
        # Pull Row and Column for agent from tuple
        agent_row = agent_initial_coordinate[0]
        agent_column = agent_initial_coordinate[1]

        # Calculate Manhattan Distance for current cell
        manhattan_distance = abs(agent_row - self.row) + abs(agent_column - self.column)

        self.g_value = manhattan_distance

    def get_coordinate(self):
        return self.row, self.column

    def get_g_value(self):
        # Return Manhattan Distance
        return self.g_value


