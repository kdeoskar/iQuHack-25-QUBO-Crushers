from dimod import BinaryQuadraticModel, ConstrainedQuadraticModel, Binary, Integer
import random
from dwave.system import LeapHybridCQMSampler
from dwave.optimization import Model
import numpy as np

cqm = ConstrainedQuadraticModel()
# bqm = BinaryQuadraticModel()
sampler = LeapHybridCQMSampler()
model = Model()

### Given ###
num_locations = 10
num_coolers = 5
num_servers = 5
amount_cooling_used = {}
amount_cooling_needed = {}

# Cooler position matrix over time
X = [[[Binary(f"{i}_{m}_{t}") for i in range(num_coolers)] for m in range(num_servers+num_coolers)] for t in range(0,12)]
# Server position matrix over time (should be fixed)
Y = [[[Binary(f"{j}_{n}_{t}") for j in range(num_servers)] for n in range(num_servers+num_coolers)] for t in range(0,12)]
# Amount of cooling provided by cooler i to server j across time
Z = [[[Integer(f"{i}_{j}_{t}") for i in range(num_coolers)] for j in range(num_servers)] for t in range(0,12)]
# Change c and r later, they should be inputted by the user
amount_cooling_used = [[Integer(f"{i}_{t}") for i in range(num_coolers)] for t in range(0,12)]
amount_cooling_needed = [[Integer(f"{j}_{t}") for j in range(num_servers)] for t in range(0,12)]
cost_to_move = [[Integer(f"{i}_{t}") for i in range(num_coolers)] for t in range(0,12)]
cost_to_stay = [[Integer(f"{i}_{t}") for i in range(num_coolers) for t in range(0,12)]]

for j in range(num_servers):
    # print(sum([amount_cooling_needed[t][j] for t in range(0,12)]))
    cqm.add_constraint(sum([sum([Z[t][j][i].linear[f"{i}_{j}_{t}"] for i in range(num_coolers)]) for t in range(0,12)]) == sum([amount_cooling_needed[t][j] for t in range(0,12)]))
for i in range(num_coolers):
    cqm.add_constraint(sum([sum([Z[t][j][i].linear[f"{i}_{j}_{t}"] for j in range(num_servers)]) for t in range(0,12)]) == sum([amount_cooling_used[t][i] for t in range(0,12)]))
print(X[0][0][0].linear["0_0_0"])
print(float(sum([sum([sum([X[t][m][i].linear[f"{i}_{m}_{t}"] for i in range(num_coolers)]) for m in range(0, num_coolers+num_servers)]) for t in range(0,12)])))
print(float(num_coolers*(num_coolers+num_servers)*12))
cqm.add_constraint(lhs = (sum([sum([sum([X[t][m][i].linear[f"{i}_{m}_{t}"] for i in range(num_coolers)]) for m in range(num_coolers+num_servers)]) for t in range(0,12)])) ==
                   num_coolers*(num_coolers+num_servers)*12)
cqm.add_constraint(sum([sum([sum([Y[t][n][j].linear[f"{j}_{n}_{t}"] for j in range(num_servers)]) for n in range(0, num_coolers+num_servers)]) for t in range(0,12)]) == num_servers)


obj = sum([[cost_to_move[t][i] + cost_to_stay[t][i] for i in range(num_coolers)] for t in range(0,12)])

res = sampler.sample_cqm(cqm, time_limit=10.0)
res.resolve()
