from dimod import ConstrainedQuadraticModel, Binary
import random
from dwave.system import LeapHybridCQMSampler

cqm = ConstrainedQuadraticModel()
sampler = LeapHybridCQMSampler()

### Given ###
num_locations = N
num_coolers = C
num_servers = S
# List of the amount of cooling produced by each cooler
amount_cooling_used = []
# List of the amount of cooling required by each server
amount_cooling_needed = []

### Variables ###



sampler.sample_cqm(cqm)
