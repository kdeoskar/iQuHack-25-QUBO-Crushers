from dimod import BinaryQuadraticModel, ConstrainedQuadraticModel, Binary, Integer
import random
from dwave.system import LeapHybridCQMSampler
from dwave.optimization import Model

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
Z = [[[Binary(f"{i}_{j}_{t}") for i in range(num_coolers)] for j in range(num_servers)] for t in range(0,12)]
# Change c and r later, they should be inputted by the user
amount_cooling_used = [[Integer(f"{i}_{t}") for i in range(num_coolers)] for t in range(0,12)]
amount_cooling_needed = [[Integer(f"{j}_{t}") for j in range(num_servers)] for t in range(0,12)]
cost_to_move = [[Integer(f"{i}_{t}") for i in range(num_coolers)] for t in range(0,12)]
cost_to_stay = [[Integer(f"{i}_{t}") for i in range(num_coolers) for t in range(0,12)]]

for j in range(num_servers):
    # print(sum([amount_cooling_needed[t][j] for t in range(0,12)]))
    # print(sum([sum([Z[t][j][i].quadratic.values()+Z[t][j][i].linear.values() for i in range(num_coolers) if type(Z[t][j][i].quadratic.values()) == int and type(Z[t][j][i].linear.values()) == int]) for t in range(0,12)]))
    cqm.add_constraint(sum([sum([Z[t][j][i] for i in range(num_coolers)]) for t in range(0,12)]) == sum([amount_cooling_needed[t][j] for t in range(0,12)]))
for i in range(num_coolers):
    cqm.add_constraint(sum([sum([Z[t][j][i] for j in range(num_servers)]) for t in range(0,12)]) == sum([amount_cooling_used[t][i] for t in range(0,12)]))
cqm.add_constraint(sum([[[X[t][m][i] for i in range(num_coolers)] for m in range(0, num_coolers+num_servers)] for t in range(0,12)]) == num_coolers)
cqm.add_constraint(sum([[[Y[t][n][j] for j in range(num_servers)] for n in range(0, num_coolers+num_servers)] for t in range(0,12)]) == num_servers)


obj = sum([[cost_to_move[t][i] + cost_to_stay[t][i] for i in range(num_coolers)] for t in range(0,12)])

res = sampler.sample_cqm(cqm, time_limit=10.0)
res.resolve()

feasible_sampleset = res.filter(lambda d: d.is_feasible)
print(feasible_sampleset)
