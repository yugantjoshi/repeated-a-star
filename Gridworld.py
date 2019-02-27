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

screen_size = (808, 808)
width = 8
screen = pygame.display.set_mode(screen_size)

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
                pygame.display.update()
        else:
            break

    return unblocked


# essentially, we are getting the shortest path to target in this
# starting with the start_state of the agent, it adds smallest-f cell to the path
# with that cell it computes the rest of the path
# until it reaches goal, where it actually constructs the path
def computePath(start_cell, target_cell, gridworld):

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
        neighbors = []
        if(i > 0):
            neighbors.append(gridworld[i-1][j])
        if(i < (len(gridworld[0]) - 2)):
            neighbors.append(gridworld[i+1][j])
        if(j > 0):
            neighbors.append(gridworld[i][j-1])
        if(j < (len(gridworld[0]) - 2)):
            neighbors.append(gridworld[i][j+1])

        for neighbor in neighbors:
            print("neighbor:", neighbor.x, neighbor.y)

        # Set neighbors list for that cell
        curr_cell.set_neighbors(neighbors)
        neighbors = curr_cell.neighbors
        print(curr_cell.x, curr_cell.y)

        # adding the states to open_list
        for cell in neighbors:
            #if cell.visited:
             #   continue
            if cell in closed_list:
                continue
            if cell.discovered and cell.blocked:
                continue

            # update value if already exists in open_list
            for cell_tuple in open_list:
                if cell_tuple[1].x == cell.x and cell_tuple[1].y == cell.y:
                    open_list.remove(cell_tuple)
                    heapq.heapify(open_list)
                    break

            heapq.heappush(open_list,(cell.f, cell))
            cell.discovered = True
            #print(cell.x, cell.y)
            #print(open_list)
            cell.parent = curr_cell
            #print("parent ", cell.parent.x, cell.parent.y)

    return None


def forwardAStar(agent_initial_cell, target_cell, gridworld, tie):

    start_state = agent_initial_cell
    while(1):
        path = computePath(start_state, target_cell, gridworld)

        if path is None:
            print("no path")
            return


        start_state = path[len(path)-1]

        #for cell in path:
         #   if(cell.x != agent_initial_cell.x or cell.y != agent_initial_cell.y):
                #print("path", cell.x, cell.y)
                #print(cell.parent.x, cell.parent.y)

        print("new start ", start_state.x, start_state.y)
        if start_state.x == target_cell.x and start_state.y == target_cell.y:
            break

    return
    """
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

    """

def backwardAStar(agent_initial_cell, target_cell, gridworld, tie):

    while (1):
        path = computePath(target_cell, agent_initial_cell, gridworld)

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
                #########
                agent_initial_cell.x = 0

                while agent_initial_cell.blocked:
                    agent_initial_cell = rand.choice(rand.choice(gridworld))
                    ######
                    agent_initial_cell.x = 0

                pygame.draw.rect(screen, GREEN, (agent_initial_cell.x*width, agent_initial_cell.y*width, width, width))

                global target_cell

                target_cell = rand.choice(rand.choice(gridworld))
                ########
                target_cell.x = num_cols - 1

                while target_cell.blocked:
                    target_cell = rand.choice(rand.choice(gridworld))
                    ########
                    target_cell.x = num_cols - 1
                    target_cell.y = num_rows - 5
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
