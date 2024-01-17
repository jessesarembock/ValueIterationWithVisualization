#program to find optimal policy for package delivery using value iteration

#import packages
import sys
import random
import numpy as np
import matplotlib.pyplot as plt
from Animate import generateAnimat

#create object of type point which holds values such as coordinates, value and reward
class gridpoint:

    action = None
    
    def __init__(self, x, y, value, reward):
        self.x = x
        self.y = y
        self.value = value
        self.reward = reward

    #method to get coordinates of gridpoint as a list
    def getCoordinates(self):
        return [self.x, self.y]

#get width and height command-line arguments
width, height = int(sys.argv[1]), int(sys.argv[2])

#set default start point
start_state = (random.randint(0, width-1), random.randint(0, height-1))

#set default end point, ensuring end point is not the same as start point
while True:
    end_state = (random.randint(0, width-1), random.randint(0, height-1))
    if end_state != start_state:
        break

k = 3 #set default number of landmines
g = 0.8 #set default value of gamma

#parse command-line arguments
n = 3
while n <= len(sys.argv) - 2:
    if sys.argv[n] == "-start":
        start_state[0], start_state[1] = int(sys.argv[n+1]), int(sys.argv[n+2])
    elif sys.argv[n] == "-end":
        end_state[0], end_state[1] = int(sys.argv[n+1]), int(sys.argv[n+2])
    elif sys.argv[n] == "-k":
        k = int(sys.argv[n+1])
    elif sys.argv[n] == "-gamma":
        g = sys.argv[n+1]
    n+=1

#setup environment
environment = []
for y in range(height):
    for x in range(width):
        if (x, y) == end_state:
            environment.append(gridpoint(x, y, 0, 100))
        else:
            environment.append(gridpoint(x, y, 0, -1))

#set landmine positions
def set_landmines(k, width, height, start_state, end_state, environment):
    all_coordinates = [(x, y) for x in range(width) for y in range(height) 
                        if (x, y) != start_state and (x, y) != end_state]
    
    #randomly select landmine positions
    landmines = random.sample(all_coordinates, k)

    #set reward values to -250 at landmine points
    for point in environment:
        if point.getCoordinates() in landmines:
            point.reward = -250
    
    return landmines
      
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

    count = 0
    for j in range(len(environment)):
        if abs(environment[j].value - old_values[j]) < theta: #check that change in value less than theta
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

    if x == 0 and y == 0:
        act = max(old_values[up], old_values[right])
        if act == old_values[up]:
            environment[point].action = 'U'
        else:
            environment[point].action = 'R'

    elif x == 0 and y == height-1:
        act = max(old_values[right], old_values[down])
        if act == old_values[right]:
            environment[point].action = 'R'
        else:
            environment[point].action = 'D'

    elif x == width-1 and y == 0:
        act = max(old_values[up], old_values[left])
        if act == old_values[up]:
            environment[point].action = 'U'
        else:
            environment[point].action = 'L'

    elif x == width-1 and y == height-1:
        act = max(old_values[down], old_values[left])
        if act == old_values[down]:
            environment[point].action = 'D'
        else:
            environment[point].action = 'L'

    elif x == 0:
        act = max(old_values[up], old_values[right], old_values[down])
        if act == old_values[up]:
            environment[point].action = 'U'
        elif act == old_values[right]:
            environment[point].action = 'R'
        else:
            environment[point].action = 'D'

    elif x == width-1:
        act = max(old_values[up], old_values[down], old_values[left])
        if act == old_values[up]:
            environment[point].action = 'U'
        elif act == old_values[down]:
            environment[point].action = 'D'
        else:
            environment[point].action = 'L'

    elif y == 0:
        act = max(old_values[up], old_values[right], old_values[left])
        if act == old_values[up]:
            environment[point].action = 'U'
        elif act == old_values[right]:
            environment[point].action = 'R'
        else:
            environment[point].action = 'L'

    elif y == height-1:
        act = max(old_values[right], old_values[down], old_values[left])
        if act == old_values[right]:
            environment[point].action = 'R'
        elif act == old_values[down]:
            environment[point].action = 'D'
        else:
            environment[point].action = 'L'

    else:
        act = max(old_values[up], old_values[right], old_values[down], old_values[left])
        if act == old_values[up]:
            environment[point].action = 'U'
        elif act == old_values[right]:
            environment[point].action = 'R'
        elif act == old_values[down]:
            environment[point].action = 'D'
        else:
            environment[point].action = 'L'

#initialize optimal policy list            
opt_pol = []

#get start state and end state from environment
for e in environment:
    if e.x == start_state[0] and e.y == start_state[1]:
        state = e
    elif e.x == end_state[0] and e.y == end_state[1]:
        end = e

#add states to optimal policy list
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
opt_pol.append((state.x, state.y))

#generate gif
landmines = set_landmines(k, width, height, start_state, end_state, environment)
anim, fig, ax = generateAnimat(records, start_state, end_state, mines = landmines, opt_pol = opt_pol, start_val = -10, end_val = 100, mine_val = 150, just_vals = False, generate_gif = False, vmin = -10, vmax = 150)
plt.show()