from dimod import BinaryQuadraticModel, ConstrainedQuadraticModel, Binary, Integer
import random
from dwave.system import LeapHybridCQMSampler
from dwave.optimization import Model
import numpy as np

cqm = ConstrainedQuadraticModel()
sampler = LeapHybridCQMSampler()
model = Model()

### Given ###
num_coolers = 5 # In our math this is C (number of closets)
num_servers = 5 # In our math this is D (number of departments)
num_locations = num_coolers+num_servers # In our math this is N (number of positions)

### Variables ###
# Cooler position matrix over time
X = [[[Integer(f"{i}_{m}_{t}") for i in range(num_coolers)] for m in range(num_locations)] for t in range(0,12)]
# Server position matrix over time (should be fixed)
Y = [[[Integer(f"{j}_{n}_{t}") for j in range(num_servers)] for n in range(num_locations)] for t in range(0,12)]
# Amount of cooling provided by cooler i to server j across time
Z = [[[Integer(f"{i}_{j}_{t}") for i in range(num_coolers)] for j in range(num_servers)] for t in range(0,12)]
# Change c and r later, they should be inputted by the user
amount_cooling_used = [[2.0 for i in range(num_coolers)] for t in range(0,12)]
amount_cooling_needed = [[2.0 for j in range(num_servers)] for t in range(0,12)]
cooler_cost_to_move = [[Integer(f"{i}_{t}") for i in range(num_coolers)] for t in range(0,12)]
cooler_cost_to_stay = [[Integer(f"{i}_{t}") for i in range(num_coolers)] for t in range(0,12)]
server_cost_to_move = [[Integer(f"{j}_{t}") for j in range(num_servers)] for t in range(0,12)]
server_cost_to_stay = [[Integer(f"{j}_{t}") for j in range(num_servers)] for t in range(0,12)]
d = [[abs(i-j) for i in range(num_coolers)] for j in range(num_servers)]
### Constraints ###
# add_constraint() needs a quadratic/linear model on one side and a constant on the other side to work
print(sum([sum([amount_cooling_used[t][i] for t in range(0,12)]) for i in range(num_coolers)]))
for j in range(num_servers):
    cqm.add_constraint(sum([sum([Z[t][j][i] for i in range(num_coolers)]) for t in range(0,12)]) == sum([sum([amount_cooling_needed[t][j] for t in range(0,12)]) for j in range(num_servers)]))
for i in range(num_coolers):
    cqm.add_constraint(sum([sum([Z[t][j][i] for j in range(num_servers)]) for t in range(0,12)]) == sum([sum([amount_cooling_used[t][i] for t in range(0,12)]) for i in range(num_coolers)]))
for t in range(0,12):
    cqm.add_constraint(sum([sum([X[t][m][i] for i in range(num_coolers)]) for m in range(num_locations)]) == num_coolers)
    cqm.add_constraint(sum([sum([Y[t][n][j] for j in range(num_servers)]) for n in range(num_locations)]) == num_servers)
for t in range(0,12):
    for m in range(num_locations):
        cqm.add_constraint(sum([sum([X[t][m][i] for m in range(num_locations)]) for i in range(num_coolers)]) + sum([sum([Y[t][m][j] for m in range(num_locations) for j in range(num_servers)])]) == 1)

### Objective Function ###
obj = sum([sum([cooler_cost_to_move[t][i] + cooler_cost_to_stay[t][i] for i in range(num_coolers)]) for t in range(0,12)])
cqm.set_objective(obj)

### Solve ###
res = sampler.sample_cqm(cqm, time_limit=10.0)
# res.resolve()
# feasible_sampleset = res.filter(lambda d: d.is_feasible)
# best_feasible = feasible_sampleset.first.sample
print(res.first.sample)
