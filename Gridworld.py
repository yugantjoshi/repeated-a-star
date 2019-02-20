import random
import pygame
import numpy as np
from Cell import Cell


def create_maze():

    #Colors
    WHITE = (255, 255, 255)
    GRAY = (20, 20, 20)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)

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
            num_chosen = random.choice(random_list)

            print(x, y)

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

    while not done:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                done = True

        screen.fill(GRAY)

        # Mark visited and current
        current_cell.set_visited(True)
        current_cell.set_current(True)

        # Draw for current cell
        for y in range(num_rows):
            for x in range(num_cols):
                draw2(gridworld[y][x])


        # Get next cell to go to
        next_cell = check_neighbors(current_cell)

        # If next cell is valid
        if next_cell != False:
            # Clear neighbors list for new cell
            current_cell.set_neighbors([])
            # add current cell to stack
            cell_stack.append(current_cell)
            # Remove walls
            # remove_walls(current_cell, next_cell)
            # Go to next cell
            current_cell.set_current(False)
            current_cell = next_cell

        # Pop new cell from remaining cells in stack
        elif len(cell_stack) > 0:
            current_cell.set_current(False)
            current_cell = cell_stack.pop()

        pygame.display.flip()
        clock.tick(60)

create_maze()