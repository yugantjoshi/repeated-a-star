
class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.blocked = False
        self.visited = False
        self.discovered = False

        self.g = 0
        self.h = 0
        self.f = 0

        self.neighbors = []
        self.parent = None

    def set_neighbors(self, neighbors):
        self.neighbors = neighbors
        for n in neighbors:
            n.g = n.g+1
            n.f = n.g + n.h

    def set_g_value(self, a_x, a_y):
        self.g = abs(a_x - self.x) + abs(a_y - self.y)
        self.f = self.g + self.h

    def set_h_value(self, t_x, t_y):
        self.h = abs(t_x - self.x) + abs(t_y - self.y)

    def __lt__(self, other):
        return self.f < other.f

    def get_coordinate(self):
        return self.x, self.y

    def get_best_neighbor(self, tie):
        minN = self.neighbors[0]

        for n in self.neighbors:
            if not n.visited and not n.blocked:
                if n.f < minN.f:
                    if n.f == minN.f:
                        # Tie Break
                        if tie:  # Use g
                            if n.g < minN.g:
                                minN = n
                        else:  # Use h
                            if n.h < minN.h:
                                minN = n
                    else:
                        minN = n
        return minN
