import numpy as np
import math

# Variables to change
strike = 30
s0 = 30
rf = 0.05
sigma = 0.30
time = 0.5 # Time in years
call = True # True or False

steps = 6
simulations = 5000

def add_extra_step(qstar,paths,up,down):
    """
    Given qstar, up, and down, simulate taking every node in paths out 1 step
    """
    new_paths = []
    for index,path in enumerate(paths):
        random = np.random.random()
        if random > (1-qstar):
            new_paths.append((path[0]*up,path[1]*qstar))
        else:
            new_paths.append((path[0]*down,path[1]*(1-qstar)))
    return new_paths

# Calculated 
stepsize = time/steps
up = math.exp(sigma * math.sqrt(stepsize))
down = 1/up
qstar = (math.exp(rf * stepsize) - down)/(up-down)


# simulate paths
paths = [[(s0,1) for _ in range(simulations)]]

for s in range(steps):
    paths.append(add_extra_step(qstar,paths[-1],up,down))


# consolidate all nodes of every path into 1 price
prices = [0 for _ in range(simulations)]
for t in paths:
    for index,node in enumerate(t):
        prices[index] += node[0]

# average out each path
# replace any above strike with payoff, any below strike with 0
for index,t in enumerate(prices):
    if call:
        if t/(steps+1) >= strike:
            prices[index] = t/(steps+1) - strike
        else:
            prices[index] = 0
    else:
        if t/(steps+1) <= strike:
            prices[index] = strike - t/(steps+1)
        else:
            prices[index] = 0

# Return average of all payoffs and discount back to present
price = sum(prices)/simulations * math.exp(-rf * time)
print(price)


    

    