closed_list = []
open_list = []

# essentially, we are getting the shortest path to target in this
# starting with the start_state of the agent, it adds smallest-f cell to the path
# with that cell it computes the rest of the path
# until it reaches goal, where it actually constructs the path
def computePath():

    closed.clear()
    open_list = []
    open_list.add(agent.get_cell)

    while(len(open) > 0):

        curr_state = open.pop

        path.add(curr_state)

        # goal reached by travelling through unexplored cells as well
        # get_path is going to take care of the blocked cells in the path
        if(curr_state == gridWorld.targetCell):
            return contructPath(curr_state, path)

        closed_list.add(curr_state)

        all_states = getAdjacent(curr_state)

        # adding the states to open_list
        for state in all_states:
            if is_in_closed(state):
                continue

            if is_in_open(state):
                update_open_list(state)

            else:
                open_list.add(state)
                open_list.heapify




def __main__():
    while(1):
        path = computePath()

        if path is None:
            print("no path")
            return

        move_to_cell = path.peekLast()
        if((move_to_cell != gridWorld.targetCell())):
            agent.set_coordinates(move_to_cell)
        else:
            break

"""
def computePath():
    while target.get_g_value() > states[0].get_g_value:
        next_state = states.pop()
        closed.append(next_state)

        up = get_vertical(curr.get_coordinate[0], next_state.get_coordinate[0])
        if(up < 0):
            down = abs(up)
            actions += down
        else:
            actions += up
        right = get_horizontal(curr.get_coordinate[1], next_state.get_coordinate[1])
        if(right < 0):
            left = abs(right)
            actions += left
        else:
            actions += right

        while actions > 0:

def get_vertical(curr_coordinate, next_coordinate):

    return
"""
"""
import heapq as Heap

count = 0
states = Heap()

curr = Cell(agent_row, agent_column)
target = Cell(target_row, target_column)

for state in states:
    state.sVal = 0

while curr != target:
    count = count+1
    curr.set_g_value(0)
    curr.sVal = count
    #g for every cell, including target, is set to -1 (infinite)
"""