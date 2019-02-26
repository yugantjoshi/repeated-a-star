import pygame
import random as rand
import numpy as np
import heapq as heap
from Cell import Cell

# Colors
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
BLACK = (0, 0, 0)
RED = (255,0,00)
GREEN = (0,250,154)
BLUE = (0,191,255)

screen_size = (707, 707)
width = 7
screen = pygame.display.set_mode(screen_size)

def forwardAStar(agent_initial_cell, target_cell, gridworld, tie):
    # True tie means prefer gval, False means prefer hval
    openlist = []
    closedlist = []
    agent_initial_cell.g = 0

    heap.heappush(openlist, (agent_initial_cell.f, agent_initial_cell))

    while len(openlist) > 0:
        current_cell_tuple = heap.heappop(openlist)
        current_cell = current_cell_tuple[1]

        #pygame.draw.rect(screen, BLUE, (current_cell.x * width, current_cell.y * width, width, width))

        heap.heappush(closedlist, current_cell_tuple)
        current_cell.visited = True
        current_cell.set_g_value(current_cell.x, current_cell.y)

        # Reached target, return shortest path list
        if current_cell.x == target_cell.x and current_cell.y == target_cell.y:
            print(closedlist)
            return get_shortest_path(agent_initial_cell.x, agent_initial_cell.y, target_cell.x, target_cell.y, gridworld), closedlist

        i = current_cell.x
        j = current_cell.y

        # Calculate all neighbors
        neighbors = [gridworld[x[0]][x[1]] for x in [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)] if
                     x[0] >= 0 and x[1] >= 0 and x[0] < len(gridworld) and x[1] < len(gridworld[0])]

        # Set neighbors list for that cell
        current_cell.set_neighbors(neighbors)

        # Add all unblocked neighbors to open list
        updated_neighbors = current_cell.neighbors
        for n in updated_neighbors:
            if not n.visited and not n.blocked:
                heap.heappush(openlist, (n.f, n))

        next_cell = current_cell.get_best_neighbor(tie)
        if next_cell.x != target_cell.x and next_cell.y != target_cell.y:
            pygame.draw.rect(screen, BLUE, (next_cell.x * width, next_cell.y * width, width, width))
            pygame.display.flip()
        next_cell.parent = (current_cell.x, current_cell.y)



def get_shortest_path(a_x, a_y, t_x, t_y, gridworld):
    '''start = gridworld[a_y][a_x]
    goal = gridworld[t_y][t_x]

    ptr = goal
    path = [goal]
    while True:
        ptr = ptr.parent
        #ptr = gridworld[ptr[0]][ptr[1]]
        path.append(ptr)
        if ptr == start:
            break
        #ptr.state = 'path'
    return path'''
    pass

def draw_cell(cell):
    if cell.blocked:
        pygame.draw.rect(screen, BLACK, (cell.x * width, cell.y * width, width, width))
    else:
        pygame.draw.rect(screen, WHITE, (cell.x * width, cell.y * width, width, width))


def create_maze():
    done = False
    clock = pygame.time.Clock()

    # Num rows and cols
    num_rows = int(screen_size[0] / width)
    num_cols = int(screen_size[1] / width)

    global stack
    stack = []
    global gridworld
    gridworld = []

    #  Create grid of cells
    for x in range(num_rows):
        gridworld.append([])
        for y in range(num_cols):
            cell = Cell(x, y)
            gridworld[x].append(cell)

    global current_cell
    current_cell = gridworld[0][0]

    # Mark cells blocked or unblocked with probability
    for x in range(num_rows):
        for y in range(num_cols):
            choice = np.random.choice(['blocked', 'unblocked'], 1, p=[0.3, 0.7])
            if choice == 'blocked':
                gridworld[x][y].blocked = True

    count = 0

    while count != 1:
        if count == 0:
            screen.fill(GRAY)

            # Mark current cell as visited
            current_cell.visited = True

            # Draw current cell
            for y in range(num_rows):
                for x in range(num_cols):
                    draw_cell(gridworld[y][x])

        if len(stack) == 0:
            if count == 0:
                global agent_initial_cell

                agent_initial_cell = rand.choice(rand.choice(gridworld))

                while agent_initial_cell.blocked:
                    agent_initial_cell = rand.choice(rand.choice(gridworld))

                pygame.draw.rect(screen, GREEN, (agent_initial_cell.x*width, agent_initial_cell.y*width, width, width))

                global target_cell

                target_cell = rand.choice(rand.choice(gridworld))

                while target_cell.blocked:
                    target_cell = rand.choice(rand.choice(gridworld))

                pygame.draw.rect(screen, RED, (target_cell.x*width, target_cell.y*width, width, width))

                for x in range(num_rows):
                    for y in range(num_cols):
                        gridworld[x][y].set_h_value(target_cell.x, target_cell.y)
            count = 1

        pygame.display.flip()

    current_cell = agent_initial_cell

    count1 = 0

    while not done:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                done = True
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN:
                pygame.time.delay(5000)

        if count1 == 0:
            forwardAStar(agent_initial_cell, target_cell, gridworld, True)
            count1 = 1;
        pygame.display.flip()
        pygame.time.delay(10)
        clock.tick(30)

create_maze()
