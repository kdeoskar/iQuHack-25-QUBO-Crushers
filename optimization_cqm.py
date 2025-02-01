from dimod import ConstrainedQuadraticModel, Binary
import random
from dwave.system import LeapHybridCQMSampler

cqm = ConstrainedQuadraticModel()
sampler = LeapHybridCQMSampler()

### Given ###
num_locations = N
num_coolers = C
num_servers = S
for t in range(0, 12):
    # Dictionary mapping the months to lists of how much cooling each cooler provided
    amount_cooling_used = {t: [0 for i in range(num_coolers)]}
    # Dictionary mapping the months to lists of how much cooling each server needed
    amount_cooling_needed = {t: [0 for i in range(num_servers)]}

### Variables ###
for t in range(0, 12):
    # Dictionary mapping the months to lists that map each cooler to its location at that month. A 1 means the cooler i was at server j
    cooler_location = {t: [0 for i in range(num_coolers) for j in range(num_servers)]}
    # Dictionary mapping the months to lists that map how much cooling each cooler i provided to server j during that month
    cooling_provided = {t: [0 for i in range(num_coolers) for j in range(num_servers)]}

### Constraints ###
cost_per_server = []
cooling_total_per_server = []
for j in range(num_servers):
    cooling_total_per_server[j] = sum(amount_cooling_needed[t][j] for t in range(0, 12))
    for t in range(0, 12):
        cost_per_server[j] = sum(cooling_provided[t][i*j] for i in range(num_coolers))

### Cost ###
cost_to_move_cooler = 10
cost_to_run = 5
for i in range(num_coolers):
    for t in range(0, 12):
        # Dictionary mapping the months to lists of how much it would cost to move each server
        cost_to_move = {t: [cost_to_move_cooler for j in range(num_servers)]}
        # Dictionary mapping the months to lists of how much it would cost to keep the cooler running
        cost_to_keep = {t: [cost_to_run for i in range(num_coolers)]}
for t in range(0, 12):
    cost_total = sum(cost_to_move[t]) + sum(cost_to_keep[t])

sampler.sample_cqm(cqm)
