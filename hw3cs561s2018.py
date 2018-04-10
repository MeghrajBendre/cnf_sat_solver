import copy
from enum import Enum
import time
start_time = time.time()


class directions(Enum):
    up_walk = [(1,0),(0,-1),(0,1),(1,0),(0,-1),(0,1)]         #up,left,right
    left_walk = [(0,-1),(-1,0),(1,0),(0,-1),(-1,0),(1,0)]      #left,down,up
    right_walk = [(0,1),(1,0),(-1,0),(0,1),(1,0),(-1,0)]      #right,up,down
    down_walk = [(-1,0),(0,-1),(0,1),(-1,0),(0,-1),(0,1)]      #down,left,right
    up_run = [(2,0),(0,-2),(0,2),(1,0),(0,-1),(0,1)]
    left_run = [(0,-2),(-2,0),(2,0),(0,-1),(-1,0),(1,0)]
    right_run = [(0,2),(2,0),(-2,0),(0,1),(1,0),(-1,0)]
    down_run = [(-2,0),(0,-2),(0,2),(-1,0),(0,-1),(0,1)]


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
    t_pos_reward = []
    for i in range(wall_no + 3, wall_no + 3 + t_no):
        t = ip[i].split(",")
        temp_t = []
        temp_t.append(int(t[0])-1)                
        temp_t.append(int(t[1])-1)
        temp_t.append(float(t[2]))
        t_pos_reward.append(temp_t)
    
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

    cntr = 0
    for i in range(0, obj.rows):
        for j in range(0, obj.cols):
            k = str(i) + "_" + str(j)

            if obj.grid.has_key(k):
                cntr += 1
                #print cntr
                for direction in directions:
                    action(i,j,obj,k,direction)
                    #print type(obj.grid[k][direction.name])
            



        
            else:   #if state is not in the grid
                continue
    
    #for x in obj.grid['0_0']:
    #    print x,obj.grid['0_0'][x]

def action(i, j, obj, k, direction): #list from the dict, x is 1 (walk) or 2 (run)

#UP
    temp_tup = {}
    if obj.grid.has_key(str(i+direction.value[0][0]) + "_" + str(j+direction.value[0][1])) and obj.grid.has_key(str(i+direction.value[3][0]) + "_" + str(j+direction.value[3][1])):
        if direction.name[-3:] == 'run':
            temp_tup[str(i+direction.value[0][0]) + "_" + str(j+direction.value[0][1])] = obj.p_run
        else:
            temp_tup[str(i+direction.value[0][0]) + "_" + str(j+direction.value[0][1])] = obj.p_walk
    else:
        if direction.name[-3:] == 'run':
            temp_tup[k] = obj.p_run
        else:
            temp_tup[k] = obj.p_walk

    if obj.grid[k][direction.name].has_key(temp_tup.keys()[0]):
        obj.grid[k][direction.name][temp_tup.keys()[0]] += temp_tup.values()[0]
    else:
        obj.grid[k][direction.name].update(temp_tup)

#LEFT
    temp_tup = {}
    if obj.grid.has_key(str(i+direction.value[1][0]) + "_" + str(j+direction.value[1][1])) and obj.grid.has_key(str(i+direction.value[4][0]) + "_" + str(j+direction.value[4][1])):
        if direction.name[-3:] == 'run':
            temp_tup[str(i+direction.value[1][0]) + "_" + str(j+direction.value[1][1])] = (0.5 * (1 - obj.p_run))
        else:
            temp_tup[str(i+direction.value[1][0]) + "_" + str(j+direction.value[1][1])] = (0.5 * (1 - obj.p_walk))
    else:
        if direction.name[-3:] == 'run':
            temp_tup[k] = (0.5 * (1 - obj.p_run))#obj.p_run
        else:
            temp_tup[k] = (0.5 * (1 - obj.p_walk))#obj.p_walk


    if obj.grid[k][direction.name].has_key(temp_tup.keys()[0]):
        obj.grid[k][direction.name][temp_tup.keys()[0]] += temp_tup.values()[0]
    else:
        obj.grid[k][direction.name].update(temp_tup)

#RIGHT
    temp_tup = {}
    if obj.grid.has_key(str(i+direction.value[2][0]) + "_" + str(j+direction.value[2][1])) and obj.grid.has_key(str(i+direction.value[5][0]) + "_" + str(j+direction.value[5][1])):
        if direction.name[-3:] == 'run':
            temp_tup[ str(i+direction.value[2][0]) + "_" + str(j+direction.value[2][1])] = (0.5 * (1 - obj.p_run))
        else:
            temp_tup[ str(i+direction.value[2][0]) + "_" + str(j+direction.value[2][1])] = (0.5 * (1 - obj.p_walk))

    else:
        if direction.name[-3:] == 'run':
            temp_tup[k] = (0.5 * (1 - obj.p_run)) #obj.p_run
        else:
            temp_tup[k] = (0.5 * (1 - obj.p_walk)) #obj.p_walk

    if obj.grid[k][direction.name].has_key(temp_tup.keys()[0]):
        obj.grid[k][direction.name][temp_tup.keys()[0]] += temp_tup.values()[0]
    else:
        obj.grid[k][direction.name].update(temp_tup)

def generate_grid(obj):

    #Generate keys for the grid first
    for i in range(0, obj.rows):
        for j in range(0, obj.cols):
            k = str(i) + "_" + str(j)
            obj.grid[k] = {"up_walk":{},"left_walk":{},"right_walk":{},"down_walk":{},"up_run":{},"left_run":{},"right_run":{},"down_run":{}}

    #print len(obj.grid)
    #remove states having walls from the grid
    for i in range(0, obj.wall_no):
        k = str(obj.wall_pos[i][0]) + "_" + str(obj.wall_pos[i][1])
        if obj.grid.has_key(k):
            obj.grid.pop(k)
    print len(obj.grid)

    #add corresponding probabilities to each move
    generate_inital_trasitions(obj)    


def main():
    obj = read_input_file()
    #writing to the output file
    op = open("output.txt","w")
    check_values_in_object(obj)
    generate_grid(obj)


    op.close()
    print("--- %s seconds ---" % (time.time() - start_time))

#call to main function
if __name__ == '__main__':
    main()