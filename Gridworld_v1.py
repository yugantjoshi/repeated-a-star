import pygame
import random as rand
import numpy as np
import heapq
from Cell_v1 import Cell

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

global discovered_nodes_count


# gets a potential path from compute path (thru cell.parent)
# constructs path until the first unblocked and resets the start position of agent
# colors the path taken
"constructPath()::- builds the shortestPath and colors it BLUE"
def constructPath(start_cell, target_cell):
    path = []

    path.append(target_cell)
    curr_cell = target_cell.parent
    while curr_cell is not start_cell:
        path.append(curr_cell)
        curr_cell = curr_cell.parent

    path.append(start_cell)

    unblocked = []

    for curr_cell in reversed(path):
        if not curr_cell.blocked:
            unblocked.append(curr_cell)
            curr_cell.visited = True
            if curr_cell != start_cell and curr_cell != target_cell:
                pygame.draw.rect(screen, BLUE, (curr_cell.x * width, curr_cell.y * width, width, width))
        else:
            break

    return unblocked

# essentially, we are getting the shortest path to target in this
# starting with the start_state of the agent, it adds smallest-f cell to the path
# with that cell it computes the rest of the path
# until it reaches goal, where it actually constructs the path
"computePathForward()::- finds a path from the start_cell to target_cell using forwardAStar"
def computePathForward(start_cell, target_cell, gridworld, tie):
    global discovered_nodes_count
    closed_list = []
    open_list = []
    start_cell.g = 0
    heapq.heappush(open_list, (start_cell.f, start_cell))

    while(len(open_list) > 0):

        curr_cell_tuple = heapq.heappop(open_list)
        curr_cell = curr_cell_tuple[1]


        # goal reached by travelling through unexplored cells as well
        # get_path is going to take care of the blocked cells in the path
        if(curr_cell.x == target_cell.x and curr_cell.y == target_cell.y):
            return constructPath(start_cell, curr_cell), closed_list

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
                discovered_nodes_count += 1
                pygame.draw.rect(screen, PURPLE, (cell.x * width, cell.y * width, width, width))
            cell.parent = curr_cell

    return None

# essentially, we are getting the shortest path to target in this
# starting with the start_state of the agent, it adds smallest-f cell to the path
# with that cell it computes the rest of the path
# until it reaches goal, where it actually constructs the path
"computePathBackward()::- finds a path from the start_cell to target_cell using backwardAStar"
def computePathBackward(start_cell, target_cell, gridworld, tie):
    global discovered_nodes_count
    closed_list = []
    open_list = []
    target_cell.h = 0
    heapq.heappush(open_list, (target_cell.f, target_cell))

    while(len(open_list) > 0):

        curr_cell_tuple = heapq.heappop(open_list)
        curr_cell = curr_cell_tuple[1]


        # goal reached by travelling through unexplored cells as well
        # get_path is going to take care of the blocked cells in the path
        if(curr_cell.x == start_cell.x and curr_cell.y == start_cell.y):
            return constructPath(target_cell, curr_cell)

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
                        if cell.h < minGval.h:
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
                discovered_nodes_count += 1
                pygame.draw.rect(screen, PURPLE, (cell.x * width, cell.y * width, width, width))
            cell.parent = curr_cell
    return None

"forwardAStar()::- Runs the Forward A* search"
def forwardAStar(agent_initial_cell, target_cell, gridworld, tie):

    start_state = agent_initial_cell
    while(1):
        path,closed_list = computePathForward(start_state, target_cell, gridworld, tie)

        if path is None:
            print("no path")
            return None, None
        start_state = path[len(path)-1]

        if start_state.x == target_cell.x and start_state.y == target_cell.y:
            return path, closed_list

    return None, None

"backwardAStar()::- Runs the Backward A* search"
def backwardAStar(agent_initial_cell, target_cell, gridworld, tie):

    while (1):
        path = computePathBackward(agent_initial_cell, target_cell, gridworld, tie)

        if path is None:
            print("no path")
            return

        agent_initial_cell = path[len(path) - 1]
        if agent_initial_cell.x == target_cell.x and agent_initial_cell.y == target_cell.y:
            break

"adaptiveAstar()::- Runs the AdaptiveA* search"
def adaptiveAstar(start_cell, target_cell, gridworld, tie):
    global discovered_nodes_count

    while(1):

        path, closedlist = forwardAStar(start_cell, target_cell, gridworld, tie)

        if path is None:
            print("No possible path")
            return
        cost = len(path)-1
        reset_maze(gridworld, True)
        gridworld[agent_initial_cell.x][agent_initial_cell.y].g = 0
        gridworld[target_cell.x][target_cell.y].h = 0

        for cell in closedlist:
            cell.setHNewVal(cost)

        closedlist = []
        openlist = []

        heapq.heappush(openlist, (start_cell.f, start_cell))

        while(len(openlist) > 0):
            curr_cell_tuple = heapq.heappop(openlist)
            curr_cell = curr_cell_tuple[1]

            if curr_cell.x == target_cell.x and curr_cell.y == target_cell.y:
                path_tuple =  constructPath(start_cell, curr_cell), closedlist
                return path_tuple

            closedlist.append(curr_cell)

            i = curr_cell.x
            j = curr_cell.y
            print(i,j)
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

            curr_cell.set_neighbors(neighbors)
            curr_cell.set_Aneighbors(neighbors, target_cell, cost)
            neighbors = curr_cell.neighbors

            for cell in neighbors:
                if cell in closedlist:
                    continue
                if cell.discovered or cell.blocked:
                    continue
                for cell_tuple in openlist:
                    if cell_tuple[1].x == cell.x and cell_tuple[1].y == cell.y:
                        openlist.remove(cell_tuple)
                        heapq.heapify(openlist)
                        break
                if len(openlist) != 0:
                    minGval = heapq.heappop(openlist)
                    minGval = minGval[1]

                    if cell.f == minGval.f:
                        # Tie Break
                        if tie:  # Use small g
                            if cell.g < minGval.g:
                                heapq.heappush(openlist, (minGval.f, minGval))
                                minGval = cell
                                heapq.heappush(openlist, (minGval.f, minGval))
                            else:
                                heapq.heappush(openlist, (minGval.f, minGval))
                                heapq.heappush(openlist, (cell.f, cell))
                        else:  # Use Large g
                            '''if cell.h < minGval.h:
                                heapq.heappush(open_list, (minGval.f, minGval))
                                minGval = cell
                                heapq.heappush(open_list, (minGval.f, minGval))'''

                    else:
                        heapq.heappush(openlist, (minGval.f, minGval))
                        heapq.heappush(openlist,(cell.f, cell))
                else:
                    heapq.heappush(openlist, (cell.f, cell))

                cell.discovered = True
                if cell != start_cell and cell != target_cell:
                    discovered_nodes_count += 1
                    pygame.draw.rect(screen, PURPLE, (cell.x * width, cell.y * width, width, width))
                cell.parent = curr_cell
        print("EXIT")
        return None


"draw_cell()::- Colors the bloced cells BLACK and unblocked cells WHITE"
def draw_cell(cell):
    if cell.blocked:
        pygame.draw.rect(screen, BLACK, (cell.x * width, cell.y * width, width, width))
    else:
        pygame.draw.rect(screen, WHITE, (cell.x * width, cell.y * width, width, width))

"create_maze()::- Generates a maze with randomly blocked and unblocked cells"
def create_maze():

    # Num rows and cols
    num_rows = int(screen_size[0] / width)
    num_cols = int(screen_size[1] / width)

    global stack
    stack = []
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

"create_agent_target()::- Randomly places the Agent and the Target on the maze"
def create_agent_target(gridworld):


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

    return (agent_initial_cell, target_cell)

"start_game()::- Begins the pygame for visualization"
def start_game(agent_initial_cell, target_cell, gridworld, forward_backward_adaptive, gridcount):
    done = False
    clock = pygame.time.Clock()
    count1 = 0

    while not done:
        '''for e in pygame.event.get():
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    if forward_backward_adaptive == 0:
                        pygame.image.save(screen, "Forward_Grid_%d.jpeg" % gridcount)
                    elif forward_backward_adaptive == 1:
                        pygame.image.save(screen, "Backward_Grid_%d.jpeg" % gridcount)
                    elif forward_backward_adaptive == 2:
                        pygame.image.save(screen, "Adaptive_Grid_%d.jpeg" %gridcount)
                    done = True
            if e.type == pygame.QUIT:
                done = True
                break'''

        if count1 == 0:
            if forward_backward_adaptive == 0:
                forwardAStar(agent_initial_cell, target_cell, gridworld, True)
            elif forward_backward_adaptive == 1:
                backwardAStar(agent_initial_cell, target_cell, gridworld, True)
            elif forward_backward_adaptive == 2:
                final_a_path = adaptiveAstar(agent_initial_cell, target_cell, gridworld, True)
                print(final_a_path[0])
            if forward_backward_adaptive == 0:
                print("Discovered: %d nodes in Forward A*" % discovered_nodes_count)
                pygame.image.save(screen, "Forward_Grid_%d.jpeg" % gridcount)

                f_forward = open("Log_Forward_A_Star.txt", "a+")
                f_forward.write("Forward A* Discovered: %d\r\n" % discovered_nodes_count)
                f_forward.close()
                done = True
            elif forward_backward_adaptive == 1:
                print("Discovered: %d nodes in Backward A*" % discovered_nodes_count)
                pygame.image.save(screen, "Backward_Grid_%d.jpeg" % gridcount)

                f_backward = open("Log_Backward_A_Star.txt", "a+")
                f_backward.write("Backward A* Discovered: %d\r\n" % discovered_nodes_count)
                f_backward.close()
                done = True
            elif forward_backward_adaptive == 2:
                print("Discovered: %d nodes in Adaptive A*" % discovered_nodes_count)
                pygame.image.save(screen, "Adaptive_Grid_%d.jpeg" % gridcount)

                f_backward = open("Log_Adaptive_A_Star.txt", "a+")
                f_backward.write("Adaptive A* Discovered: %d\r\n" % discovered_nodes_count)
                f_backward.close()
                done = True
                pass

            count1 = 1
        pygame.display.flip()
        pygame.time.delay(10)
        clock.tick(30)

"set_hg_in_maze()::- Depending on forward or backward sets the H or G values in the maze"
def set_hg_in_maze(generated_maze, hVal):

    if hVal:
        num_rows = int(screen_size[0] / width)
        num_cols = int(screen_size[1] / width)

        for x in range(num_rows):
            for y in range(num_cols):
                generated_maze[x][y].set_h_value(target_cell.x, target_cell.y)

    else:
        num_rows = int(screen_size[0] / width)
        num_cols = int(screen_size[1] / width)

        for x in range(num_rows):
            for y in range(num_cols):
                generated_maze[x][y].set_g_value(agent_initial_cell.x, agent_initial_cell.y)

"reset_maze()::- Reset each cell in the maze to its original configuration"
def reset_maze(generated_maze, adaptive):
    agent_initial_cell
    num_rows = int(screen_size[0] / width)
    num_cols = int(screen_size[1] / width)

    for x in range(num_rows):
        for y in range(num_cols):
            if generated_maze[x][y].discovered or generated_maze[x][y].visited:
                generated_maze[x][y].reset_cell(adaptive)
                pygame.draw.rect(screen, WHITE, (x * width, y * width, width, width))
    pygame.draw.rect(screen, GREEN, (agent_initial_cell.x * width, agent_initial_cell.y * width, width, width))
    pygame.draw.rect(screen, RED, (target_cell.x * width, target_cell.y * width, width, width))



"Runs the program 50 to generate 50 screenshots of the forward and backward searches"
for create_fifty in range(11 ):
    generated_maze = create_maze()
    complete_maze = create_agent_target(generated_maze)
    set_hg_in_maze(generated_maze, True)  # True to run forward A*
    discovered_nodes_count = 0
    start_game(complete_maze[0], complete_maze[1], generated_maze, 0, create_fifty)
    reset_maze(generated_maze, False)
    set_hg_in_maze(generated_maze, False)  # False to run backward A*
    discovered_nodes_count = 0
    start_game(complete_maze[0], complete_maze[1], generated_maze, 1, create_fifty)
    reset_maze(generated_maze, True)
    discovered_nodes_count = 0
    set_hg_in_maze(generated_maze, True)  # True to run forward A*
    start_game(complete_maze[0], complete_maze[1], generated_maze, 2, create_fifty)
