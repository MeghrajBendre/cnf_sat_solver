import copy

directions = {
"up_walk":[(1,0),(0,-1),(0,1)],         #up,left,right
"left_walk":[(0,-1),(-1,0),(1,0)],      #left,down,up
"right_walk":[(0,1),(1,0),(-1,0)],      #right,up,down
"down_walk":[(-1,0),(0,-1),(0,1)],      #down,left,right
"up_run":[(2,0),(0,-2),(0,2)],
"left_run":[(0,-2),(-2,0),(2,0)],
"right_run":[(0,2),(2,0),(-2,0)],
"down_run":[(-2,0),(0,-2),(0,2)]}


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
        temp_wall.append(int(t[0]))
        temp_wall.append(int(t[1]))
        wall_pos.append(temp_wall)

    #get terminal state number, position and rewards
    t_no = int(ip[2+wall_no])
    t_pos_reward = []
    for i in range(wall_no + 3, wall_no + 3 + t_no):
        t = ip[i].split(",")
        temp_t = []
        temp_t.append(int(t[0]))                
        temp_t.append(int(t[1]))
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

    for i in range(0, obj.rows):
        for j in range(0, obj.cols):
            k = str(i) + "_" + str(j)

            if obj.grid.has_key(k):
                for direction in directions:
                    #print direction,directions[direction]
                    action(i,j,1,obj,k,direction)
                    
            



        
            else:   #if state is not in the grid
                continue
    
    for x in obj.grid:
        print x, obj.grid[x]

def action(i, j, x, obj, k, direction): #list from the dict, x is 1 (walk) or 2 (run)
    ######ADD CHECK FOR 2 i.e. if the middle state is present or not
#UP
    if obj.grid.has_key(str(i+directions[direction][0][0]) + "_" + str(j+directions[direction][0][1])):
        temp_tup = (obj.p_walk, str(i+directions[direction][0][0]) + "_" + str(j+directions[direction][0][1]))
    else:
        temp_tup = (obj.p_walk, k)
    obj.grid[k][direction].append(temp_tup)

#LEFT
    if obj.grid.has_key(str(i+directions[direction][1][0]) + "_" + str(j+directions[direction][1][1])):
        temp_tup = (0.5 * (1 - obj.p_walk), str(i+directions[direction][1][0]) + "_" + str(j+directions[direction][1][1]))
    else:
        temp_tup = (0.5 * (1 - obj.p_walk), k)
    obj.grid[k][direction].append(temp_tup)

#RIGHT
    if obj.grid.has_key(str(i+directions[direction][2][0]) + "_" + str(j+directions[direction][2][1])):
        temp_tup = (0.5 * (1 - obj.p_walk), str(i+directions[direction][2][0]) + "_" + str(j+directions[direction][2][1]))
    else:
        temp_tup = (0.5 * (1 - obj.p_walk), k)
    obj.grid[k][direction].append(temp_tup)





'''def action_down(list, x):
def action_left(list, x):    
def action_right(list, x):'''

def generate_grid(obj):

    #Generate keys for the grid first
    for i in range(0, obj.rows):
        for j in range(0, obj.cols):
            k = str(i) + "_" + str(j)
            obj.grid[k] = {"up_walk":[],"left_walk":[],"right_walk":[],"down_walk":[],"up_run":[],"left_run":[],"right_run":[],"down_run":[]}

    #remove states having walls from the grid
    for i in range(0, obj.wall_no):
        k = str(obj.wall_pos[i][0]) + "_" + str(obj.wall_pos[i][1])
        if obj.grid.has_key(k):
            obj.grid.pop(k)

    #add corresponding probabilities to each move
    generate_inital_trasitions(obj)    


def main():
    obj = read_input_file()
    #writing to the output file
    op = open("output.txt","w")
    #check_values_in_object(obj)
    generate_grid(obj)

    op.close()


#call to main function
if __name__ == '__main__':
    main()