import copy

class Grid:
    def __init__(self, rows, cols, wall_no, wall_pos, t_no, t_pos_reward, p_walk, p_run, r_walk, r_run, discount):
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
        

#reads input file and does necessary formatting
def read_input_file():

    input_file = open("input.txt")
    ip = input_file.read().splitlines()
    print ip

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
    temp_obj = Grid(rows, cols, wall_no, wall_pos, t_no, t_pos_reward, p_walk, p_run, r_walk, r_run, discount)

    return temp_obj

def check_values_in_object(obj):
    print obj.rows
    print obj.cols
    print obj.wall_no
    print obj.wall_pos
    print obj.t_no
    print obj.t_pos_reward
    print obj.p_walk
    print obj.p_run
    print obj.r_walk
    print obj.r_run
    print obj.discount  

def main():
    obj = read_input_file()
    #writing to the output file
    op = open("output.txt","w")
    #check_values_in_object(obj)

    op.close()


#call to main function
if __name__ == '__main__':
    main()