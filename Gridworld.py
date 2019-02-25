import random
import pygame
import numpy as np
from Cell import Cell



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

    done = False
    clock = pygame.time.Clock()

    # Num cols and rows based on screen size and width
    num_rows = int(screen_size[1] / WIDTH)
    num_cols = int(screen_size[0] / WIDTH)

    cell_stack = []

    def draw(cell):
        if cell.get_current:
            pygame.draw.rect(screen, RED, (cell.get_row(), cell.get_column(), WIDTH, WIDTH))
        elif cell.get_visited():
            pygame.draw.rect(screen, WHITE, (cell.get_row(), cell.get_column(), WIDTH, WIDTH))
            choice = np.random.choice(['unblocked', 'blocked'],
                                 1,
                                 p=[0.3, 0.7])
            print(choice)
            if choice == 'blocked':
                pygame.draw.rect(screen, BLACK, (cell.get_row(), cell.get_column(), WIDTH, WIDTH))
            elif choice == 'unblocked':
                pygame.draw.rect(screen, WHITE, (cell.get_row(), cell.get_column(), WIDTH, WIDTH))

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


    def remove_walls(current_cell, next_cell):
        pass

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
                        gridworld[y][x].set_g_value(agent)
                        gridworld[y][x].set_h_value(target)
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

        '''As the agent Moves along the path update within this loop and color path that is taken'''

        color_next_cell = pick_next_cell(curr_cell, end_cell, WIDTH)

        if color_next_cell != target:
            pygame.draw.rect(screen, BLUE, (color_next_cell[0], color_next_cell[1], WIDTH, WIDTH))

        curr_cell = color_next_cell


        pygame.display.flip()
        pygame.time.delay(100)
        #clock.tick(6000)

agent = ()
target = ()
create_maze(agent, target)