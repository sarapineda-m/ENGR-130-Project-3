import math
import robotbit_library as r
from microbit import *
import radio 

chnl = 3
    
radio.config(channel=chnl)
radio.on()
    
M1A = 0x1  
M2B = 0x4  

r.setup()

x_size = 5
y_size = 3
grid_map = [
    [1, 1, 1],
    [2, 0, 1],
    [1, 0, 2],
    [1, 0, 1],
    [1, 0, 99],
]

def turnRight90():
    r.motor(M1A, 100)
    r.motor(M2B, 100)
    sleep(217)
    r.motor(M1A, 0)
    r.motor(M2B, 0)

def turnLeft90():
    r.motor(M1A, -100)
    r.motor(M2B, -100)
    sleep(217)
    r.motor(M1A, 0)
    r.motor(M2B, 0)

def moveForward(numBlocks):
    powerSetting = [40,0]    # list of power settings, in pct, to cycle through
    for pwr_sig in powerSetting:
        r.motor(M1A,-1*pwr_sig)
        r.motor(M2B,1.05*pwr_sig)
        print("Power signal = {}".format(pwr_sig))
        sleep(1400)    

s = radio.receive()                    # receive direction command

if s == "L":
    grid_map[1][0] = 2
    grid_map[2][2] = 1
    display.show("O")
if s == "R":
    grid_map[2][2] = 2
if s == "O":
    grid_map[1][0] = 2
    grid_map[2][2] = 2
if s == "X":
    display.show("No spots open!")                   # receive direction command


def wavefrontSearch():
    
    start_x, start_y = None, None
    for x in range(x_size):
        for y in range(y_size):
            if grid_map[x][y] == 99:
                start_x, start_y = x, y
                break
        if start_x is not None:
            break

    current_wave = 2
    found_wave = True
    while found_wave:
        found_wave = False
        for y in range(y_size):
            for x in range(x_size):
                if grid_map[x][y] == current_wave:
                    found_wave = True
                    for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < x_size and 0 <= ny < y_size:
                            if grid_map[nx][ny] == 0:
                                grid_map[nx][ny] = current_wave + 1
        current_wave += 1
        sleep(500)

  
    if start_x is not None and start_y is not None:
        grid_map[start_x][start_y] = 99

def navigateToGoal():
    
    robot_pos = None
    for x in range(x_size):
        for y in range(y_size):
            if grid_map[x][y] == 99:
                robot_pos = (x, y)
                break
        if robot_pos:
            break

    if robot_pos is None:
        raise ValueError("Robot position (99) not found in grid_map")

    current_dir = 0
    x, y = robot_pos

    while True:
        min_val = float('inf')
        next_dir = current_dir
        next_pos = (x, y)

        for direction, (dx, dy) in enumerate([(0,1), (1,0), (0,-1), (-1,0)]):
            nx, ny = x + dx, y + dy
            if 0 <= nx < x_size and 0 <= ny < y_size:
                if grid_map[nx][ny] < min_val and grid_map[nx][ny] >= 2:
                    min_val = grid_map[nx][ny]
                    next_pos = (nx, ny)
                    next_dir = direction

        dir_diff = (next_dir - current_dir) % 4
        if dir_diff == 1:
            turnRight90()
            sleep(1000)
        elif dir_diff == 3:
            turnLeft90()
            sleep(1000)
        elif dir_diff == 2:
            turnRight90()
            sleep(1000)
            turnRight90()
            sleep(1000)

        moveForward(1)
        
        x, y = next_pos
        current_dir = next_dir

        if grid_map[x][y] == 2:
            break

    
sleep(1000)
print(grid_map)
wavefrontSearch()
navigateToGoal()

while True:
    sleep(1000)

