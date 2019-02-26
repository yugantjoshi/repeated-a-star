
class Cell():

    def __init__(self, row, col, width):

        self.row = row * width
        self.col = col * width

        self.x = col
        self.y = row

        self.visited = False
        self.current = False

        self.is_blocked = False

        self.g_value = -1
        self.h_value = -1
        self.f_value = -1

        self.walls = [True, True, True, True]  # top , right , bottom , left

        # neighbors
        self.neighbors = []

        self.top = 0
        self.right = 0
        self.bottom = 0
        self.left = 0

        self.parent = ()

    def set_top(self, top):
        self.top = top

    def set_bottom(self, bottom):
        self.bottom = bottom

    def set_right(self, right):
        self.right = right

    def set_left(self, left):
        self.left = left

    def set_neighbors(self, neighbors):
        self.neighbors = neighbors
        for n in neighbors:
            n.set_g_value = self.g_value+1
            self.update_f_value()


    def set_x(self, x):
        self.x = x
    def set_y(self, y):
        self.y = y
    def get_x(self):
        return self.x
    def get_y(self):
        return self.y
    def add_neighbor(self, s):
        self.neighbors.append(s)

    def set_visited(self, isVisited):
        self.visited = isVisited

    def set_current(self, isCurrent):
        self.current = isCurrent

    def set_is_blocked(self, is_blocked):
        self.is_blocked = is_blocked

    def set_parent(self, cell):
        self.parent = cell

    def set_g_value(self, agent_coordinate):
        # Pull Row and Column for agent from tuple
        agent_row = agent_coordinate[0]
        agent_column = agent_coordinate[1]

        # Calculate Manhattan Distance for current cell
        manhattan_distance = abs(agent_row - self.y) + abs(agent_column - self.x)

        self.g_value = manhattan_distance
        self.f_value = self.g_value + self.h_value

    def set_h_value(self, target_coordinate):
        # Pull Row and Column for target from tuple
        target_row = target_coordinate[0]
        target_column = target_coordinate[1]

        # Calculate Manhattan Distance for current cell
        manhattan_distance = abs(target_row - self.x) + abs(target_column - self.y)

        self.h_value = manhattan_distance

    def update_f_value(self):
        self.f_value = self.g_value + self.h_value

    def __lt__(self, other):
        return self.get_f_value() < other.get_f_value()

    def get_coordinate(self):
        return self.x, self.y

    def get_visited(self):
        return self.visited

    def get_current(self):
        return self.current

    def get_row(self):
        return self.row

    def get_column(self):
        return self.col

    def get_is_blocked(self):
        return self.is_blocked

    def get_g_value(self):
        # Return Manhattan Distance
        return self.g_value

    def get_h_value(self):
        return self.h_value

    def get_f_value(self):
        return self.f_value

    def get_neighbors(self):
        return self.neighbors

    def get_neighbor(self, i):
        return self.neighbors[i]

    def get_parent(self):
        return self.parent

    def get_top(self):
        return self.top

    def get_bottom(self):
        return self.bottom

    def get_right(self):
        return self.right

    def get_left(self):
        return self.left

    def get_best_neighbor(self, tie):
        # Return neighbor with the smallest f value
        minNeighbor = self.neighbors[0]
        for n in self.neighbors:
            if not n.get_visited():
                if n.get_f_value() < minNeighbor.get_f_value():
                    if n.get_f_value() == minNeighbor.get_f_value():
                        # Tie Break
                        if tie:  # use gval
                            if n.get_g_value() < minNeighbor.get_g_value():
                                minNeighbor = n
                            #pass
                        else:  # use hval
                            if n.get_h_value() < minNeighbor.get_h_value():
                                minNeighbor = n
                            #pass
                    else:
                        minNeighbor = n
        return minNeighbor




