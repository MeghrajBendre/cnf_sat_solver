import copy
from enum import Enum
import time
start_time = time.time()

priority = [["Walk_Up",0],["Walk_Down",0],["Walk_Left",0],["Walk_Right",0],["Run_Up",0],["Run_Down",0],["Run_Left",0],["Run_Right",0],]


class directions(Enum):
    Walk_Up = [(1,0),(0,-1),(0,1),(1,0),(0,-1),(0,1)]         #up,left,right
    Walk_Left = [(0,-1),(-1,0),(1,0),(0,-1),(-1,0),(1,0)]      #left,down,up
    Walk_Right = [(0,1),(1,0),(-1,0),(0,1),(1,0),(-1,0)]      #right,up,down
    Walk_Down = [(-1,0),(0,-1),(0,1),(-1,0),(0,-1),(0,1)]      #down,left,right
    Run_Up = [(2,0),(0,-2),(0,2),(1,0),(0,-1),(0,1)]
    Run_Left = [(0,-2),(-2,0),(2,0),(0,-1),(-1,0),(1,0)]
    Run_Right = [(0,2),(2,0),(-2,0),(0,1),(1,0),(-1,0)]
    Run_Down = [(-2,0),(0,-2),(0,2),(-1,0),(0,-1),(0,1)]


class Grid:
    def __init__(self, rows, cols, wall_no, wall_pos, t_no, t_pos_reward, p_walk, p_run, r_walk, r_run, discount, grid):
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
        #print str(int(t[0])-1) + "_" + str(int(t[1])-1)
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
    temp_obj = Grid(rows, cols, wall_no, wall_pos, t_no, t_pos_reward, p_walk, p_run, r_walk, r_run, discount, {})

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
            if obj.grid.has_key(k):
                for direction in directions:
                    if direction.name[-1] == 'n':
                        action_run(i,j,obj,k,direction)
                    else:
                        action_walk(i,j,obj,k,direction)
                    #print type(obj.grid[k][direction.name])
            

            else:   #if state is not in the grid
                continue
    



def action_walk(i, j, obj, k, direction): #list from the dict, x is 1 (walk) or 2 (run)

#UP
    temp_tup = {}
    z_key = str(i+direction.value[0][0]) + "_" + str(j+direction.value[0][1]) 
    if obj.grid.has_key(z_key):
            temp_tup[z_key] = obj.p_walk
    else:
            temp_tup[k] = obj.p_walk

    if obj.grid[k][direction.name].has_key(temp_tup.keys()[0]):
        obj.grid[k][direction.name][temp_tup.keys()[0]] += temp_tup.values()[0]
    else:
        obj.grid[k][direction.name].update(temp_tup)

#LEFT
    temp_tup = {}
    z_key = str(i+direction.value[1][0]) + "_" + str(j+direction.value[1][1])
    if obj.grid.has_key(z_key):
            temp_tup[z_key] = (0.5 * (1 - obj.p_walk))
    else:
            temp_tup[k] = (0.5 * (1 - obj.p_walk))#obj.p_walk

    if obj.grid[k][direction.name].has_key(temp_tup.keys()[0]):
        obj.grid[k][direction.name][temp_tup.keys()[0]] += temp_tup.values()[0]
    else:
        obj.grid[k][direction.name].update(temp_tup)

#RIGHT
    temp_tup = {}
    z_key = str(i+direction.value[2][0]) + "_" + str(j+direction.value[2][1])
    if obj.grid.has_key(z_key):
            temp_tup[z_key] = (0.5 * (1 - obj.p_walk))
    else:
            temp_tup[k] = (0.5 * (1 - obj.p_walk)) #obj.p_walk

    if obj.grid[k][direction.name].has_key(temp_tup.keys()[0]):
        obj.grid[k][direction.name][temp_tup.keys()[0]] += temp_tup.values()[0]
    else:
        obj.grid[k][direction.name].update(temp_tup)





def action_run(i, j, obj, k, direction): #list from the dict, x is 1 (walk) or 2 (run)

#UP
    temp_tup = {}
    z_key = str(i+direction.value[0][0]) + "_" + str(j+direction.value[0][1]) 
    if obj.grid.has_key(z_key) and obj.grid.has_key(str(i+direction.value[3][0]) + "_" + str(j+direction.value[3][1])):
            temp_tup[z_key] = obj.p_run
    else:
            temp_tup[k] = obj.p_run

    if obj.grid[k][direction.name].has_key(temp_tup.keys()[0]):
        obj.grid[k][direction.name][temp_tup.keys()[0]] += temp_tup.values()[0]
    else:
        obj.grid[k][direction.name].update(temp_tup)

#LEFT
    temp_tup = {}
    z_key = str(i+direction.value[1][0]) + "_" + str(j+direction.value[1][1])
    if obj.grid.has_key(z_key) and obj.grid.has_key(str(i+direction.value[4][0]) + "_" + str(j+direction.value[4][1])):
            temp_tup[z_key] = (0.5 * (1 - obj.p_run))
    else:
            temp_tup[k] = (0.5 * (1 - obj.p_run))#obj.p_run

    if obj.grid[k][direction.name].has_key(temp_tup.keys()[0]):
        obj.grid[k][direction.name][temp_tup.keys()[0]] += temp_tup.values()[0]
    else:
        obj.grid[k][direction.name].update(temp_tup)

#RIGHT
    temp_tup = {}
    z_key = str(i+direction.value[2][0]) + "_" + str(j+direction.value[2][1])
    if obj.grid.has_key(z_key) and obj.grid.has_key(str(i+direction.value[5][0]) + "_" + str(j+direction.value[5][1])):
            temp_tup[z_key] = (0.5 * (1 - obj.p_run))

    else:
            temp_tup[k] = (0.5 * (1 - obj.p_run)) #obj.p_run

    if obj.grid[k][direction.name].has_key(temp_tup.keys()[0]):
        obj.grid[k][direction.name][temp_tup.keys()[0]] += temp_tup.values()[0]
    else:
        obj.grid[k][direction.name].update(temp_tup)






def generate_grid(obj):

    #Generate keys for the grid first
    for i in range(0, obj.rows):
        for j in range(0, obj.cols):
            k = str(i) + "_" + str(j)
            obj.grid[k] = {"Walk_Up":{},"Walk_Down":{},"Walk_Left":{},"Walk_Right":{},"Run_Up":{},"Run_Down":{},"Run_Left":{},"Run_Right":{}}

    #remove states having walls from the grid
    for i in range(0, obj.wall_no):
        k = str(obj.wall_pos[i][0]) + "_" + str(obj.wall_pos[i][1])
        obj.grid.pop(k,None)

    generate_inital_trasitions(obj) 

    #remove terminal states
    for terminal in obj.t_pos_reward.keys():
        obj.grid[terminal] = {"Walk_Up":{},"Walk_Down":{},"Walk_Left":{},"Walk_Right":{},"Run_Up":{},"Run_Down":{},"Run_Left":{},"Run_Right":{}}
        #print obj.grid[terminal]
    #add corresponding probabilities to each move


    #for x in obj.grid.keys():
       # print x,obj.grid[x],"\n"
   

def calculate_max(state, current_position, U2, discount, terminal_states):
    max_value = float("-inf")
    global priority

    #if it is a terminal state, add only reward associated with it
    if current_position in terminal_states.keys():
        return terminal_states[current_position], "Exit" 

    for i in range(0,8):
        sum = 0
        for key in state[priority[i][0]].keys():            
            sum +=  (state[priority[i][0]][key] * (priority[i][1] + discount * U2[key]))            
        if max_value < sum:
            max_value = sum
            max_value_step = priority[i][0]

 

    return max_value, max_value_step

def value_iteration(obj):
    U1={}
    moves = {}
    epsilon = 0.001

    for key in obj.grid.keys():
        U1[key] = float(0.0)

    while True:
        U2 = copy.deepcopy(U1)
        delta = 0

        for state in obj.grid.keys():
            U1[state], moves[state] = calculate_max(obj.grid[state], state, U1, obj.discount, obj.t_pos_reward)
            delta = max(delta, abs(U1[state] - U2[state]))

        if delta < (epsilon * (1 - obj.discount) / obj.discount):
            break
    
    final_ans = []
    for i in range(0,obj.rows):
        ans = []
        for j in range(0,obj.cols):
            k=str(i) + "_" + str(j)
            if k in moves.keys():
                #print moves[k]
                m1 = (moves[k]).split("_")
                if len(m1) == 2:
                    m2 = m1[0] + " " + m1[1]
                    ans.append(m2)
                else:
                    ans.append(m1[0])
            else:
                #print "None"
                ans.append("None")
        final_ans.append(ans)
    
    for i in range(len(final_ans)-1,-1,-1):
        for j in range(0,len(final_ans[i])):
            print str(final_ans[i][j]) + ",",
        print ""

    
    exit()

def main():
    obj = read_input_file()
    #writing to the output file
    op = open("output.txt","w")
    #check_values_in_object(obj)
    generate_grid(obj)
    value_iteration(obj)

    op.close()
    print("--- %s seconds ---" % (time.time() - start_time))

#call to main function
if __name__ == '__main__':
    main()