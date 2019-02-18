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
    WIDTH = 70
    screen = pygame.display.set_mode(screen_size)

    done = False

    # Num cols and rows based on screen size and width
    num_rows = int(screen_size[1] / WIDTH)
    num_cols = int(screen_size[0] / WIDTH)

    cell_stack = []

    def draw(cell):
        if cell.get_current:
            pygame.draw.rect(screen, RED, (cell.get_row(), cell.get_column(), WIDTH, WIDTH))
        elif cell.get_visited():
            choice = np.random.choice(['unblocked', 'blocked'],
                                 1,
                                 p=[0.3, 0.7])
            print(choice)
            if choice == 'blocked':
                pygame.draw.rect(screen, BLACK, (cell.get_row(), cell.get_column(), WIDTH, WIDTH))
            elif choice == 'unblocked':
                pygame.draw.rect(screen, WHITE, (cell.get_row(), cell.get_column(), WIDTH, WIDTH))


    def check_neighbors(cell):
        if int(cell.get_column() / WIDTH) - 1 >= 0:
            cell.set_top(gridworld[int(cell.get_column() / WIDTH) - 1][int(cell.get_row() / WIDTH)])

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
                draw(gridworld[y][x])

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

create_maze()