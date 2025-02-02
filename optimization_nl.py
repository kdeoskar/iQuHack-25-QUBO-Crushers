import dimod
import random
from dwave.system import LeapHybridNLSampler
from dwave.optimization import Model

model = Model()

weights = model.constant([6, 5, 30, 25, 70])
values = model.constant([5, 17, 50, 30, 56])
capacity = model.constant(30)

items = model.set(5)
model.add_constraint(weights[items].sum() <= capacity)

model.minimize(-values[items].sum())

sampler = LeapHybridNLSampler()
sampler.sample(model)

model.states.resize(2)
items.set_state(0, [0, 1])
items.set_state(1, [0, 2, 3])

with model.lock():
    print(model.objective.state(0) > model.objective.state(1))
    print(model.objective.state(0))
    print(model.objective.state(1))
