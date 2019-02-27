import pygame
import random as rand
import numpy as np
import heapq
from Cell import Cell

# Colors
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
BLACK = (0, 0, 0)
RED = (255,0,00)
GREEN = (0,250,154)
BLUE = (0,191,255)
PURPLE = (187,76,255)

screen_size = (808, 808)
width = 8
screen = pygame.display.set_mode(screen_size)

open_list = []
closed_list = []
# gets a potential path from compute path (thru cell.parent)
# constructs path until the first unblocked and resets the start position of agent
# colors the path taken
def constructPath(start_cell, target_cell):

    print("ENTERED CONSTRUCTPATH", start_cell.x, start_cell.y)
    path = []

    path.append(target_cell)
    curr_cell = target_cell.parent
    #print("target parent", curr_cell.x, curr_cell.y)
    while curr_cell is not start_cell:
        #print("parent", curr_cell.x, curr_cell.y)
        path.append(curr_cell)
        curr_cell = curr_cell.parent

    path.append(start_cell)

    #print(path)
    unblocked = []

    for curr_cell in reversed(path):
        if not curr_cell.blocked:
            unblocked.append(curr_cell)
            curr_cell.visited = True
            if curr_cell != start_cell and curr_cell != target_cell:
                pygame.draw.rect(screen, BLUE, (curr_cell.x * width, curr_cell.y * width, width, width))
                #pygame.display.flip()
        else:
            break

    return unblocked


# essentially, we are getting the shortest path to target in this
# starting with the start_state of the agent, it adds smallest-f cell to the path
# with that cell it computes the rest of the path
# until it reaches goal, where it actually constructs the path
def computePath(start_cell, target_cell, gridworld, tie):

    print("ENTERED COMPUTE PATH")
    print(start_cell.x, start_cell.y)
    print(target_cell.x, target_cell.y)
    closed_list = []
    open_list = []
    start_cell.g = 0
    heapq.heappush(open_list, (start_cell.f, start_cell))

    while(len(open_list) > 0):

        curr_cell_tuple = heapq.heappop(open_list)
        curr_cell = curr_cell_tuple[1]
        #print(curr_cell.x, curr_cell.y)


        # goal reached by travelling through unexplored cells as well
        # get_path is going to take care of the blocked cells in the path
        if(curr_cell.x == target_cell.x and curr_cell.y == target_cell.y):
            print("start", start_cell.x, start_cell.y)
            print("target", target_cell.x, target_cell.y)
            print("parent", curr_cell.parent.x, curr_cell.parent.y)
            return constructPath(start_cell, curr_cell)

        closed_list.append(curr_cell)

        i = curr_cell.x
        j = curr_cell.y
        # Calculate all neighbors
        neighbors = [gridworld[x[0]][x[1]] for x in [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)] if
                     x[0] >= 0 and x[1] >= 0 and x[0] < len(gridworld) and x[1] < len(gridworld[0])]

        # Set neighbors list for that cell
        curr_cell.set_neighbors(neighbors)
        neighbors = curr_cell.neighbors

        # adding the states to open_list
        for cell in neighbors:
            #if cell.visited:
             #   continue
            if cell in closed_list:
                continue
            if cell.discovered or cell.blocked:
                continue

            # update value if already exists in open_list
            for cell_tuple in open_list:
                if cell_tuple[1].x == cell.x and cell_tuple[1].y == cell.y:
                    open_list.remove(cell_tuple)
                    heapq.heapify(open_list)
                    break

            if len(open_list) != 0:
                minGval = heapq.heappop(open_list)
                minGval = minGval[1]

                if cell.f == minGval.f:
                    # Tie Break
                    if tie:  # Use small g
                        if cell.g < minGval.g:
                            heapq.heappush(open_list, (minGval.f, minGval))
                            minGval = cell
                            heapq.heappush(open_list, (minGval.f, minGval))
                        else:
                            heapq.heappush(open_list, (minGval.f, minGval))
                            heapq.heappush(open_list, (cell.f, cell))
                    else:  # Use Large g
                        '''if cell.h < minGval.h:
                            heapq.heappush(open_list, (minGval.f, minGval))
                            minGval = cell
                            heapq.heappush(open_list, (minGval.f, minGval))'''

                else:
                    heapq.heappush(open_list, (minGval.f, minGval))
                    heapq.heappush(open_list,(cell.f, cell))
            else:
                heapq.heappush(open_list, (cell.f, cell))

            cell.discovered = True
            if cell != start_cell and cell != target_cell:
                pygame.draw.rect(screen, PURPLE, (cell.x * width, cell.y * width, width, width))
            #print(cell.x, cell.y)
            #print(open_list)
            cell.parent = curr_cell
            #print("parent ", cell.parent.x, cell.parent.y)

    return None


def forwardAStar(agent_initial_cell, target_cell, gridworld, tie):

    start_state = agent_initial_cell
    while(1):
        path = computePath(start_state, target_cell, gridworld, tie)

        if path is None:
            print("no path")
            return


        start_state = path[len(path)-1]

        for cell in path:
            if(cell.x != agent_initial_cell.x or cell.y != agent_initial_cell.y):
                print("path", cell.x, cell.y)
                print(cell.parent.x, cell.parent.y)

        print("new start ", start_state.x, start_state.y)
        if start_state.x == target_cell.x and start_state.y == target_cell.y:
            break

    return


def backwardAStar(agent_initial_cell, target_cell, gridworld, tie):

    while (1):
        path = computePath(target_cell, agent_initial_cell, gridworld, tie)

        if path is None:
            print("no path")
            return

        agent_initial_cell = path[len(path) - 1]
        print("new start ", agent_initial_cell.x, agent_initial_cell.y)
        if agent_initial_cell.x == target_cell.x and agent_initial_cell.y == target_cell.y:
            break


def draw_cell(cell):
    if cell.blocked:
        pygame.draw.rect(screen, BLACK, (cell.x * width, cell.y * width, width, width))
    else:
        pygame.draw.rect(screen, WHITE, (cell.x * width, cell.y * width, width, width))


def create_maze():

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

    # Mark cells blocked or unblocked with probability
    for x in range(num_rows):
        for y in range(num_cols):
            choice = np.random.choice(['blocked', 'unblocked'], 1, p=[0.3, 0.7])
            if choice == 'blocked':
                gridworld[x][y].blocked = True

    count = 0

    while count != 1:
        if count == 0:
            #screen.fill(GRAY)

            # Mark current cell as visited
            #current_cell.visited = True

            # Draw current cell
            for y in range(num_rows):
                for x in range(num_cols):
                    draw_cell(gridworld[y][x])

        if len(stack) == 0:

            count = 1


        #pygame.display.flip()

    return gridworld

def create_agent_target(gridworld):

    num_rows = int(screen_size[0] / width)
    num_cols = int(screen_size[1] / width)

    global agent_initial_cell

    agent_initial_cell = rand.choice(rand.choice(gridworld))

    #########
    #agent_initial_cell.x = 0

    while agent_initial_cell.blocked:
        agent_initial_cell = rand.choice(rand.choice(gridworld))
        ######
        #agent_initial_cell.x = 0

    pygame.draw.rect(screen, GREEN, (agent_initial_cell.x * width, agent_initial_cell.y * width, width, width))

    global target_cell

    target_cell = rand.choice(rand.choice(gridworld))

    ########
    #target_cell.x = num_cols - 1

    while target_cell.blocked:
        target_cell = rand.choice(rand.choice(gridworld))
        ########
        #target_cell.x = num_cols - 1
        # target_cell.y = num_rows - 5
    pygame.draw.rect(screen, RED, (target_cell.x * width, target_cell.y * width, width, width))

    for x in range(num_rows):
        for y in range(num_cols):
            gridworld[x][y].set_h_value(target_cell.x, target_cell.y)

    return (agent_initial_cell, target_cell)

def start_game(agent_initial_cell, target_cell, gridworld):
    done = False
    clock = pygame.time.Clock()
    count1 = 0

    while not done:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                done = True
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN:
                print("running again")
                done = True
                pygame.time.delay(5000)

        if count1 == 0:
            forwardAStar(agent_initial_cell, target_cell, gridworld, True)
            #backwardAStar(agent_initial_cell, target_cell, gridworld, True)
            count1 = 1
        pygame.display.flip()
        pygame.time.delay(10)
        clock.tick(30)

generated_maze = create_maze()
complete_maze = create_agent_target(generated_maze)
start_game(complete_maze[0], complete_maze[1], generated_maze)
#start_game(complete_maze[0], complete_maze[1], generated_maze)
#start_game(complete_maze[0], complete_maze[1], generated_maze)

