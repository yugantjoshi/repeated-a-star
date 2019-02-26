import random
import pygame
import numpy as np
import heapq as heap
from Cell import Cell


#Colors
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
BLACK = (0, 0, 0)
RED = (178,34,34)
GREEN = (34,139,34)
BLUE = (0,191,255)

# Screen Settings
screen_size = (700, 700)
WIDTH = 7
screen = pygame.display.set_mode(screen_size)


def forwardAStar(agent_initial_coord, target_coord, gridworld, tie):
    # True tie means prefer gval when choosing tied neighbors
    # False tie means prefer hval when choosing tied neighbors

    openlist = []
    closedlist = []
    start_cell = gridworld[agent_initial_coord[0]][agent_initial_coord[1]]

    heap.heappush(openlist, (start_cell.get_f_value(), start_cell))

    while len(openlist) > 0:

        current_cell = heap.heappop(openlist)[1]

        pygame.draw.rect(screen, BLUE, (current_cell.get_x(), current_cell.get_y(), WIDTH, WIDTH))

        heap.heappush(closedlist, current_cell)
        current_cell.set_visited(True)

        if current_cell.get_x() == target_coord[0] and current_cell.get_y() == target_coord[1]:
            return closedlist

        # Look at neighbors neighbors
        i = current_cell.get_x()
        j = current_cell.get_y()

        # Get all neighbors for current cell
        neighbors = [gridworld[x[1]][x[0]] for x in [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)] if
                     x[0] >= 0 and x[1] >= 0 and x[0] < len(gridworld) and x[1] < len(gridworld[0])]

        # Set neighbors list for that cell
        current_cell.set_neighbors(neighbors)
        # Take neighbor with smallest f value and add to open list
        next_cell = current_cell.get_best_neighbor(tie)
        heap.heappush(openlist, next_cell)



def pick_next_cell(curr_cell, target_cell, width):

    row = 0
    col = 0

    flag = True

    if curr_cell == target_cell:
        return curr_cell

    if curr_cell[0] < target_cell[0]:
        row = curr_cell[0] + width
        col = curr_cell[1]
        flag = False
    elif curr_cell[0] > target_cell[0]:
        row = curr_cell[0] - width
        col = curr_cell[1]
        flag = False
    elif curr_cell[0] == target_cell[0]:
        row = curr_cell[0]

    if curr_cell[1] < target_cell[1] and flag:
        col = curr_cell[1] + width
        row = curr_cell[0]
    elif curr_cell[1] > target_cell[1] and flag:
        col = curr_cell[1] - width
        row = curr_cell[0]
    elif curr_cell[1] == target_cell[1]:
        col = curr_cell[1]

    next_cell = (row, col)

    return next_cell

def create_maze(agent, target):


    done = False
    clock = pygame.time.Clock()

    # Num cols and rows based on screen size and width
    num_rows = int(screen_size[1] / WIDTH)
    num_cols = int(screen_size[0] / WIDTH)

    cell_stack = []

    def draw2(cell):
        if cell.get_is_blocked():
            pygame.draw.rect(screen, BLACK, (cell.get_row(), cell.get_column(), WIDTH, WIDTH))
        else:
            pygame.draw.rect(screen, WHITE, (cell.get_row(), cell.get_column(), WIDTH, WIDTH))


    def check_neighbors(cell):

        # Top
        if int(cell.get_column() / WIDTH) - 1 >= 0:
            gridworld_x = (cell.get_column() / WIDTH) - 1
            gridworld_y = (cell.get_row() / WIDTH)
            cell.set_top(gridworld[int(gridworld_x)][int(gridworld_y)])
        # Right
        if int(cell.get_row() / WIDTH) + 1 <= num_cols - 1:
            gridworld_x = (cell.get_column() / WIDTH)
            gridworld_y = (cell.get_row() / WIDTH) + 1
            cell.set_right(gridworld[int(gridworld_x)][int(gridworld_y)])
        # Bottom
        if int(cell.get_column() / WIDTH) + 1 <= num_rows - 1:
            gridworld_x = (cell.get_column() / WIDTH) + 1
            gridworld_y = (cell.get_row() / WIDTH)
            cell.set_bottom(gridworld[int(gridworld_x)][int(gridworld_y)])
        # Left
        if int(cell.get_row() / WIDTH) - 1 >= 0:
            gridworld_x = (cell.get_column() / WIDTH)
            gridworld_y = (cell.get_row() / WIDTH) - 1
            cell.set_left(gridworld[int(gridworld_x)][int(gridworld_y)])

        # Top
        if cell.get_top() != 0:
            if cell.get_top().get_visited() == False:
                cell.add_neighbor(cell.get_top())
                cell.get_top().get_visited()
        # Right
        if cell.get_right() != 0:
            if cell.get_right().get_visited() == False:
                cell.add_neighbor(cell.get_right())
        # Bottom
        if cell.get_bottom() != 0:
            if cell.get_bottom().get_visited() == False:
                cell.add_neighbor(cell.get_bottom())
        # Left
        if cell.get_left() != 0:
            if cell.get_left().get_visited() == False:
                cell.add_neighbor(cell.get_left())

        if len(cell.get_neighbors()) > 0:
            cell.set_next_cell(cell.get_neighbor(random.randrange(0,len(cell.get_neighbors()))))
            return cell.get_next_cell()
        else:
            return False

    #Create gridworld with cells
    gridworld = []
    for y in range(num_rows):
        gridworld.append([])
        for x in range(num_cols):
            cell = Cell(x,y, WIDTH)
            gridworld[y].append(cell)

    current_cell = gridworld[0][0]

    random_list = [1, 2, 3, 4]

    for x in range(num_rows):
        for y in range(num_cols):

            num_chosen1 = random.choice(random_list)

            if num_chosen1 == 1:

                num_chosen = random.choice(random_list)

                #top
                if num_chosen == 1:
                    if x != 0:
                        gridworld[x - 1][y].set_is_blocked(True)
                #bottom
                elif num_chosen == 2:
                    if x < num_rows - 1:
                        gridworld[x + 1][y].set_is_blocked(True)
                #right
                elif num_chosen == 3:
                    if y < num_cols - 1:
                        gridworld[x][y + 1].set_is_blocked(True)
                #left
                elif num_chosen == 4:
                    if y != 0:
                        gridworld[x][y - 1].set_is_blocked(True)


    next_cell = 0

    count = 0

    '@Summary: This loop generates the maze randomly and also sets the agent and target'
    while count != 1:

        if count == 0:

            screen.fill(GRAY)

            # Mark visited and current
            current_cell.set_visited(True)
            current_cell.set_current(True)

            # Draw for current cell
            for y in range(num_rows):
                for x in range(num_cols):
                    draw2(gridworld[y][x])

        if len(cell_stack) == 0:

            if count == 0:

                agentCell = random.choice(random.choice(gridworld))
                pygame.draw.rect(screen, GREEN, (agentCell.get_row(), agentCell.get_column(), WIDTH, WIDTH))
                agent = (agentCell.get_row(), agentCell.get_column())
                print(agent)

                targetCell = random.choice(random.choice(gridworld))
                pygame.draw.rect(screen, RED, (targetCell.get_row(), targetCell.get_column(), WIDTH, WIDTH))
                target = targetCell.get_row(), targetCell.get_column()
                print(target)

                for y in range(num_rows):
                    for x in range(num_cols):
                        agent_coord = agent[0]/WIDTH, agent[1]/WIDTH
                        target_coord = target[0]/WIDTH, target[0]/WIDTH
                        gridworld[y][x].set_g_value(agent_coord)
                        gridworld[y][x].set_h_value(target_coord)
                        gridworld[y][x].update_f_value()

                count = 1

        pygame.display.flip()

    curr_cell = agent
    end_cell = target



    '@Summary: This is the loop that is constantly running behind the scenes and updates the display'
    while not done:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                done = True

        agent_coord = int(curr_cell[0] / WIDTH), int(curr_cell[1] / WIDTH)
        target_coord = int(end_cell[0] / WIDTH), int(end_cell[1] / WIDTH)

        forwardAStar(agent_coord, target_coord, gridworld, True)

        '''As the agent Moves along the path update within this loop and color path that is taken'''

        ''' color_next_cell = pick_next_cell(curr_cell, end_cell, WIDTH)

        if color_next_cell != target:
            pygame.draw.rect(screen, BLUE, (color_next_cell[0], color_next_cell[1], WIDTH, WIDTH))

        curr_cell = color_next_cell '''


        pygame.display.flip()
        pygame.time.delay(100)
        #clock.tick(6000)

agent = ()
target = ()
create_maze(agent, target)
