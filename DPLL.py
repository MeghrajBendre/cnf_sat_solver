import copy
import time
from collections import deque
import pickle
start_time = time.time()

priority = [["up_walk",0],["down_walk",0],["left_walk",0],["right_walk",0],["up_run",0],["down_run",0],["left_run",0],["right_run",0],]
print_moves = {"up_walk":"Walk Up","left_walk":"Walk Left","right_walk":"Walk Right","down_walk":"Walk Down","up_run":"Run Up","left_run":"Run Left","right_run":"Run Right","down_run":"Run Down"}
neighbours = [(1,0),(-1,0),(0,-1),(0,1),(2,0),(-2,0),(0,-2),(0,2)]
directions = {
    "up_walk" : [(1,0),(0,-1),(0,1),(1,0),(0,-1),(0,1)],            #up,left,right
    "left_walk" : [(0,-1),(-1,0),(1,0),(0,-1),(-1,0),(1,0)],        #left,down,up
    "right_walk" : [(0,1),(1,0),(-1,0),(0,1),(1,0),(-1,0)],         #right,up,down
    "down_walk" : [(-1,0),(0,-1),(0,1),(-1,0),(0,-1),(0,1)],        #down,left,right
    "up_run" : [(2,0),(0,-2),(0,2),(1,0),(0,-1),(0,1)],
    "left_run" : [(0,-2),(-2,0),(2,0),(0,-1),(-1,0),(1,0)],
    "right_run" : [(0,2),(2,0),(-2,0),(0,1),(1,0),(-1,0)],
    "down_run" : [(-2,0),(0,-2),(0,2),(-1,0),(0,-1),(0,1)],
}

class Grid:
    def __init__(self, rows, cols, wall_no, wall_pos, t_no, t_pos_reward, p_walk, p_run, r_walk, r_run, discount, grid, pairs):
        self.rows = rows
        self.cols = cols
        self.wall_no = wall_no
        self.wall_pos = copy.deepcopy(wall_pos)
        self.t_no = t_no
        self.t_pos_reward = copy.deepcopy(t_pos_reward)
        self.p_walk = p_walk
        self.p_run = p_run
        self.r_walk = r_walk
        self.r_run = r_run
        self.discount = discount
        self.grid = grid
        self.pairs = pairs

#reads input file and does necessary formatting
def read_input_file():
    global priority    
    input_file = open("input.txt")
    ip = input_file.read().splitlines()

    #get grid size i.e. rows and columns of the grid world
    grid_size = ip[0].split(",")
    rows = int(grid_size[0])
    cols = int(grid_size[1])

    #get wall cell numbers and position
    wall_no = int(ip[1])
    wall_pos = []
    for i in range(2,(wall_no + 2)):
        t =ip[i].split(",")
        temp_wall = []
        temp_wall.append(int(t[0])-1)
        temp_wall.append(int(t[1])-1)
        wall_pos.append(temp_wall)

    #get terminal state number, position and rewards
    t_no = int(ip[2+wall_no])
    t_pos_reward = {}
    for i in range(wall_no + 3, wall_no + 3 + t_no):
        t = ip[i].split(",")
        temp_t = {}
        temp_t[str(int(t[0])-1) + "_" + str(int(t[1])-1)] = (float(t[2]))
        t_pos_reward.update(temp_t)
    
    #read transition model, rewards, and discount factor
    p = ip[wall_no + 3 + t_no].split(",")
    p_walk = float(p[0])
    p_run = float(p[1])

    r = ip[wall_no + 3 + t_no + 1].split(",")
    r_walk = float(r[0])
    r_run = float(r[1])

    discount = float(ip[wall_no + 3 + t_no + 2])
    input_file.close()    

    #put all the read values in the grid world object
    temp_obj = Grid(rows, cols, wall_no, wall_pos, t_no, t_pos_reward, p_walk, p_run, r_walk, r_run, discount, {}, {})

    for i in range(0,4):
        priority[i][1] = r_walk
    for i in range(4,8):
        priority[i][1] = r_run  

    return temp_obj

def check_values_in_object(obj):
    print "Grid rows: ",obj.rows
    print "Grid cols: ",obj.cols
    print "No. of walls: ",obj.wall_no
    print "Wall positions: ",obj.wall_pos
    print "Terminal states: ",obj.t_no
    print "Terminal position and rewards: ",obj.t_pos_reward
    print "p_walk: ",obj.p_walk
    print "p_run: ",obj.p_run
    print "r_walk: ",obj.r_walk
    print "r_run: ",obj.r_run
    print "Discount: ",obj.discount  
    print "Grid: \n",obj.grid

def generate_inital_trasitions(obj):
    global directions

    for i in range(0, obj.rows):
        for j in range(0, obj.cols):
            k = str(i) + "_" + str(j)
            obj.pairs[k] = (i,j)
            if obj.grid.has_key(k):
                for direction in directions:
                    if direction[-1] == 'n':
                        action_run(i,j,obj,k,direction)
                    else:
                        action_walk(i,j,obj,k,direction)
            else:   #if state is not in the grid
                continue

def action_walk(i, j, obj, k, direction): #list from the dict, x is 1 (walk) or 2 (run)
    global directions
#UP
    temp_tup = {}
    z_key = str(i+directions[direction][0][0]) + "_" + str(j+directions[direction][0][1]) 
    if obj.grid.has_key(z_key):
            temp_tup[z_key] = obj.p_walk
    else:
            temp_tup[k] = obj.p_walk

    if obj.grid[k][direction].has_key(temp_tup.keys()[0]):
        obj.grid[k][direction][temp_tup.keys()[0]] += temp_tup.values()[0]
    else:
        obj.grid[k][direction].update(temp_tup)

#LEFT
    temp_tup = {}
    z_key = str(i+directions[direction][1][0]) + "_" + str(j+directions[direction][1][1])
    if obj.grid.has_key(z_key):
            temp_tup[z_key] = (0.5 * (1 - obj.p_walk))
    else:
            temp_tup[k] = (0.5 * (1 - obj.p_walk))#obj.p_walk

    if obj.grid[k][direction].has_key(temp_tup.keys()[0]):
        obj.grid[k][direction][temp_tup.keys()[0]] += temp_tup.values()[0]
    else:
        obj.grid[k][direction].update(temp_tup)

#RIGHT
    temp_tup = {}
    z_key = str(i+directions[direction][2][0]) + "_" + str(j+directions[direction][2][1])
    if obj.grid.has_key(z_key):
            temp_tup[z_key] = (0.5 * (1 - obj.p_walk))
    else:
            temp_tup[k] = (0.5 * (1 - obj.p_walk)) #obj.p_walk

    if obj.grid[k][direction].has_key(temp_tup.keys()[0]):
        obj.grid[k][direction][temp_tup.keys()[0]] += temp_tup.values()[0]
    else:
        obj.grid[k][direction].update(temp_tup)


def action_run(i, j, obj, k, direction): #list from the dict, x is 1 (walk) or 2 (run)
    global directions
#UP
    temp_tup = {}
    z_key = str(i+directions[direction][0][0]) + "_" + str(j+directions[direction][0][1]) 
    if obj.grid.has_key(z_key) and obj.grid.has_key(str(i+directions[direction][3][0]) + "_" + str(j+directions[direction][3][1])):
            temp_tup[z_key] = obj.p_run
    else:
            temp_tup[k] = obj.p_run

    if obj.grid[k][direction].has_key(temp_tup.keys()[0]):
        obj.grid[k][direction][temp_tup.keys()[0]] += temp_tup.values()[0]
    else:
        obj.grid[k][direction].update(temp_tup)

#LEFT
    temp_tup = {}
    z_key = str(i+directions[direction][1][0]) + "_" + str(j+directions[direction][1][1])
    if obj.grid.has_key(z_key) and obj.grid.has_key(str(i+directions[direction][4][0]) + "_" + str(j+directions[direction][4][1])):
            temp_tup[z_key] = (0.5 * (1 - obj.p_run))
    else:
            temp_tup[k] = (0.5 * (1 - obj.p_run))#obj.p_run

    if obj.grid[k][direction].has_key(temp_tup.keys()[0]):
        obj.grid[k][direction][temp_tup.keys()[0]] += temp_tup.values()[0]
    else:
        obj.grid[k][direction].update(temp_tup)

#RIGHT
    temp_tup = {}
    z_key = str(i+directions[direction][2][0]) + "_" + str(j+directions[direction][2][1])
    if obj.grid.has_key(z_key) and obj.grid.has_key(str(i+directions[direction][5][0]) + "_" + str(j+directions[direction][5][1])):
            temp_tup[z_key] = (0.5 * (1 - obj.p_run))

    else:
            temp_tup[k] = (0.5 * (1 - obj.p_run)) #obj.p_run

    if obj.grid[k][direction].has_key(temp_tup.keys()[0]):
        obj.grid[k][direction][temp_tup.keys()[0]] += temp_tup.values()[0]
    else:
        obj.grid[k][direction].update(temp_tup)

def generate_grid(obj):
    global directions
    #Generate keys for the grid first
    for i in range(0, obj.rows):
        for j in range(0, obj.cols):
            k = str(i) + "_" + str(j)
            obj.grid[k] = {"up_walk":{},"left_walk":{},"right_walk":{},"down_walk":{},"up_run":{},"left_run":{},"right_run":{},"down_run":{}}

    #remove states having walls from the grid
    for i in range(0, obj.wall_no):
        k = str(obj.wall_pos[i][0]) + "_" + str(obj.wall_pos[i][1])
        obj.grid.pop(k,None)

    generate_inital_trasitions(obj) 

    #remove terminal states
    for terminal in obj.t_pos_reward.keys():
        obj.grid[terminal] = {"up_walk":{},"left_walk":{},"right_walk":{},"down_walk":{},"up_run":{},"left_run":{},"right_run":{},"down_run":{}}

def calculate_max(state, current_position, U, discount, terminal_states):
    max_value = float("-inf")
    global priority

    #if it is a terminal state, add only reward associated with it
    if current_position in terminal_states.keys():
        return terminal_states[current_position], "Exit" 

    for i in range(0,8):
        sum = 0
        for key in state[priority[i][0]].keys():            
            sum +=  (state[priority[i][0]][key] * (priority[i][1] + discount * U[key]))    

        if max_value < sum:
            max_value = sum
            max_value_step = priority[i][0]

    return max_value, max_value_step

def value_iteration(obj, popped_pref_queue):
    U1={}
    moves = {}
    #epsilon = 1e-45
    global priority
    U1 = {state: 0 for state in obj.grid.keys()}
    moves = {state: "" for state in obj.grid.keys()}

    while True:
        delta = 0
        for state in popped_pref_queue:#Queue
        #for state in obj.grid.keys(): #Not using queue
            U2 = U1[state]                       #ASYNC
            #U2 = U1.copy()                      #SYNC
            #TERMINAL STATE
            if state in obj.t_pos_reward.keys():
                U1[state] = obj.t_pos_reward[state]
                moves[state] = "Exit" 
            else:
                utility_for_orientation = []
                for i in range(0,8):
                    sum = 0
                    for key in obj.grid[state][priority[i][0]].keys():            
                        sum +=  (obj.grid[state][priority[i][0]][key] * (priority[i][1] + obj.discount * U1[key])) #ASYNC
                        #sum +=  (obj.grid[state][priority[i][0]][key] * (priority[i][1] + obj.discount * U2[key]))  #SYNC
                    utility_for_orientation.append(sum)
                U1[state] = max(utility_for_orientation)
                moves[state] = priority[utility_for_orientation.index(U1[state])][0]
            delta = max(delta, abs(U1[state] - U2))     #ASYNC
            #delta = max(delta, abs(U1[state] - U2[state]))    #SYNC

        #if delta < (epsilon * (1 - obj.discount) / obj.discount):
        if delta == 0:
            return U1, moves

def best_policy(obj,U):
    global priority
    moves = {}

    for state in obj.grid.keys():
        max_val_move = ""
        max_val = -1 * float("inf")
        
        for i in range(0,8):
            sum = 0
            for key in obj.grid[state][priority[i][0]].keys(): 
                sum +=  (obj.grid[state][priority[i][0]][key] * (priority[i][1] + obj.discount * U[key]))    
            if max_val < sum:
                max_val = sum
                max_val_move = priority[i][0]

        temp_dict = {}
        temp_dict[state] = max_val_move
        moves.update(temp_dict)

    return moves

def create_queue(obj):

    pref_queue = deque()
    popped_pref_queue = []
    visited = {}

    #Put terminals in the queue
    terminals = sorted(obj.t_pos_reward.values(),reverse=True)
    for terminal in terminals:
        for key, value in obj.t_pos_reward.iteritems(): 
            if value == terminal:
                pref_queue.append(key)

    #without queue
    '''for terminal in obj.t_pos_reward.values():
        for key, value in obj.t_pos_reward.iteritems(): 
            if value == terminal:
                pref_queue.append(key)'''


    while (pref_queue):
        x = pref_queue.popleft()
        if not (visited.has_key(x)):
            popped_pref_queue.append(x)
            visited[x] = 0
            
            for i in range(0,8):
                y = str(obj.pairs[x][0]+neighbours[i][0]) + "_" + str(obj.pairs[x][1]+neighbours[i][1])
                if (obj.grid.has_key(y)):
                    pref_queue.append(y)
    return popped_pref_queue

def main():
    obj = read_input_file()
    #check_values_in_object(obj)
    generate_grid(obj)
    popped_pref_queue = create_queue(obj)
    final_utility, moves = value_iteration(obj, popped_pref_queue)
    #moves = best_policy(obj,final_utility)

    
    wall_pos = {}
    for x in obj.wall_pos:
        k = str(x[0]) + "_" + str(x[1])
        wall_pos[k] = 0

    op = open("output.txt","w")
    output_record = []
    for row in range(obj.rows):
        output_row = []
        for column in range(obj.cols):
            state = str(row) + "_" + str(column)
            if state in wall_pos.keys():
                output_row.append("None")
            elif state in obj.t_pos_reward.keys():
                output_row.append("Exit")
            else:
                output_row.append(print_moves[moves[state]])
        output_record.append(",".join(output_row))
    
    final_output_record = reversed(output_record)
    op.write("\n".join(final_output_record))
    op.close()
    #print("--- %s seconds ---" % (time.time() - start_time))

#call to main function
if __name__ == '__main__':
    main()