class Cell:

    def __init__(self, row, column):
        self.row = row
        self.column = column
        self.is_blocked = False
        self.g_value = -1
        self.h_value = -1
        self.f_value = -1

    def set_is_blocked(self, is_blocked):
        self.is_blocked = is_blocked

    def set_g_value(self, agent_coordinate):
        # Pull Row and Column for agent from tuple
        agent_row = agent_coordinate[0]
        agent_column = agent_coordinate[1]

        # Calculate Manhattan Distance for current cell
        manhattan_distance = abs(agent_row - self.row) + abs(agent_column - self.column)

        self.g_value = manhattan_distance

    def set_h_value(self, target_coordinate):
        # Pull Row and Column for target from tuple
        target_row = target_coordinate[0]
        target_column = target_coordinate[1]

        # Calculate Manhattan Distance for current cell
        manhattan_distance = abs(target_row - self.row) + abs(target_column - self.column)

        self.h_value = manhattan_distance

    def set_f_value(self):
        self.f_value = self.g_value+self.h_value

    def get_coordinate(self):
        return self.row, self.column

    def get_is_blocked(self):
        return self.is_blocked

    def get_g_value(self):
        # Return Manhattan Distance
        return self.g_value

    def get_h_value(self):
        return self.h_value

    def get_f_value(self):
        return self.f_value


