#program to find optimal policy for package delivery using value iteration

#import packages
import sys
import random
import numpy as np
import matplotlib.pyplot as plt
from Animate import generateAnimat

if len(sys.argv) < 3:
    print("Error: must enter width and height values. Usage: python ValueIteration.py "
          "<width> <height> [-start <x> <y>] [-end <x> <y>] [-k <number of landmines>] [-gamma <value of gamma>]")
    sys.exit(1)

#create object of type point which holds values such as coordinates, value and reward
class GridPoint:

    def __init__(self, x, y, value, reward, action = None):
        self.x = x
        self.y = y
        self.value = value
        self.reward = reward
        self.action = action

    #method to get coordinates of gridpoint as a list
    def getCoordinates(self):
        return [self.x, self.y]

#get width and height command-line arguments
width, height = int(sys.argv[1]), int(sys.argv[2])

#set default start point
start_state = [random.randint(0, width-1), random.randint(0, height-1)]

#set default end point, ensuring end point is not the same as start point
while True:
    end_state = [random.randint(0, width-1), random.randint(0, height-1)]
    if end_state != start_state:
        break

k = 3 #set default number of landmines
g = 0.8 #set default value of gamma

#parse command-line arguments
n = 3
while n <= len(sys.argv) - 2:
    
    if sys.argv[n] == "-start":
        start_state[0], start_state[1] = int(sys.argv[n+1]), int(sys.argv[n+2])
        if not 0 <= start_state[0] < width or not 0 <= start_state[1] < height:
            print("Error: start state must be within the grid")
            sys.exit(1)

    elif sys.argv[n] == "-end":
        end_state[0], end_state[1] = int(sys.argv[n+1]), int(sys.argv[n+2])
        if not 0 <= end_state[0] < width or not 0 <= end_state[1] < height:
            print("Error: end state must be within the grid")
            sys.exit(1)

    elif sys.argv[n] == "-k":
        k = int(sys.argv[n+1])
        if k > 0.4*width*height:
            print("Error: number of landmines must be less than 40% of the grid size")
            sys.exit(1)

    elif sys.argv[n] == "-gamma":
        g = sys.argv[n+1]

    n+=1

#setup environment
environment = []
for y in range(height):
    for x in range(width):
        if [x, y] == end_state:
            environment.append(GridPoint(x, y, 0, 100))
        else:
            environment.append(GridPoint(x, y, 0, -1))

#set landmine positions
landmines = []
counter = 0
while counter < k:
    while True:
        landmine = [random.randint(0, width-1), random.randint(0, height-1)]
        if landmine != start_state and landmine != end_state and landmine not in landmines:
            landmines.append(landmine)
            break
    counter += 1

#set reward values to -250 at landmine points
for point in environment:
    for landmine in landmines:
        if landmine == point.getCoordinates():
            point.reward = -250

#create list to store values of previous iteration
old_values = []
for n in range(len(environment)):
    old_values.append(0)

#set theta value for convergence
theta = 0.01

#create records list
records = []

#value iteration using Bellman's equation
while True:

    record = []

    for point in range(len(environment)):

        x, y = environment[point].x, environment[point].y
        r = environment[point].reward
        up, right, down, left = width*(y+1) + x, width*y + (x+1), width*(y-1) + x, width*y + (x-1)

        if x == 0 and y == 0:
            environment[point].value = max(r + g*old_values[up], r + g*old_values[right])

        elif x == 0 and y == height-1:
            environment[point].value = max(r + g*old_values[right], r + g*old_values[down])

        elif x == width-1 and y == 0:
            environment[point].value = max(r + g*old_values[up], r + g*old_values[left])

        elif x == width-1 and y == height-1:
            environment[point].value = max(r + g*old_values[down], r + g*old_values[left])

        elif x == 0:
            environment[point].value = max(r + g*old_values[up], r + g*old_values[right], r + g*old_values[down])

        elif x == width-1:
            environment[point].value = max(r + g*old_values[up], r + g*old_values[down], r + g*old_values[left])

        elif y == 0:
            environment[point].value = max(r + g*old_values[up], r + g*old_values[right], r + g*old_values[left])

        elif y == height-1:
            environment[point].value = max(r + g*old_values[right], r + g*old_values[down], r + g*old_values[left])

        else:
           environment[point].value = max(r + g*old_values[up], r + g*old_values[right], r + g*old_values[down], r + g*old_values[left])

    #check for convergence
    count = 0
    for j in range(len(environment)):
        if abs(environment[j].value - old_values[j]) < theta:
            count += 1
        old_values[j] = environment[j].value
        record.append(old_values[j])

    #convert record to 2D array
    record2D = [[0 for cols in range(width)] for rows in range(height)]
    element = 0
    for i in range(height):
        for j in range(width):
            record2D[i][j] = record[element]
            element += 1
    records.append(record2D)

    if count == len(environment): #converged
        break
        
#policy extraction
for point in range(len(environment)):

    x, y = environment[point].x, environment[point].y
    up, right, down, left = width*(y+1) + x, width*y + (x+1), width*(y-1) + x, width*y + (x-1)
    action_mapping = {up: 'U', right: 'R', down: 'D', left: 'L'}

    if x == 0 and y == 0:
        # Find the action index with the maximum value
        max_action_index = max([up, right], key=lambda idx: old_values[idx])

        # Set the action for the current point based on the mapping
        environment[point].action = action_mapping[max_action_index]

    elif x == 0 and y == height-1:
        max_action_index = max([right, down], key=lambda idx: old_values[idx])
        environment[point].action = action_mapping[max_action_index]

    elif x == width-1 and y == 0:
        max_action_index = max([up, left], key=lambda idx: old_values[idx])
        environment[point].action = action_mapping[max_action_index]

    elif x == width-1 and y == height-1:
        max_action_index = max([down, left], key=lambda idx: old_values[idx])
        environment[point].action = action_mapping[max_action_index]

    elif x == 0:
        max_action_index = max([up, right, down], key=lambda idx: old_values[idx])
        environment[point].action = action_mapping[max_action_index]

    elif x == width-1:
        max_action_index = max([up, down, left], key=lambda idx: old_values[idx])
        environment[point].action = action_mapping[max_action_index]

    elif y == 0:
        max_action_index = max([up, right, left], key=lambda idx: old_values[idx])
        environment[point].action = action_mapping[max_action_index]

    elif y == height-1:
        max_action_index = max([right, down, left], key=lambda idx: old_values[idx])
        environment[point].action = action_mapping[max_action_index]

    else:
        max_action_index = max([up, right, down, left], key=lambda idx: old_values[idx])
        environment[point].action = action_mapping[max_action_index]

#initialize optimal policy list            
opt_pol = []

#get start state and end state from environment
for e in environment:
    if e.x == start_state[0] and e.y == start_state[1]:
        state = e
    elif e.x == end_state[0] and e.y == end_state[1]:
        end = e

#add states to optimal policy list
max_iterations = 999999
iterations = 0

while state != end:

    opt_pol.append((state.x, state.y))

    if state.action == 'U':
        state = environment[width*(state.y+1) + state.x]

    elif state.action == 'R':
        state = environment[width*state.y + (state.x+1)]

    elif state.action == 'D':
        state = environment[width*(state.y-1) + state.x]

    else:
        state = environment[width*state.y + (state.x-1)]

    iterations += 1

    if iterations > max_iterations:
        print("Error: maximum iterations reached. Too many landmines blocking path to end state.")
        sys.exit(1)

opt_pol.append((state.x, state.y))

#generate gif
anim, fig, ax = generateAnimat(
    
    records,
    start_state,
    end_state,
    mines=landmines,
    opt_pol=opt_pol,
    start_val=-10,
    end_val=100,
    mine_val=150,
    just_vals=False,
    generate_gif=False,
    vmin=-10,
    vmax=150

)

plt.show()