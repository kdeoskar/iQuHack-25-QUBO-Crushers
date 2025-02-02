from dwave.system import LeapHybridCQMSampler
from dimod import Binary, ConstrainedQuadraticModel, Real, quicksum

C = 10  # Numer of coolers
D = 5  # Number of servers
T = 6  # Number of time steps

# Index/Position/Time
x = [
    [[Binary(f"x_{i}_{m}_{t}") for t in range(T)] for m in range(C + D)]
    for i in range(C)
]
y = [
    [[Binary(f"y_{j}_{n}_{t}") for t in range(T)] for n in range(C + D)]
    for j in range(D)
]
z = [[[Binary(f"z_{j}_{i}_{t}") for t in range(T)] for i in range(C)] for j in range(D)]

# Multiplication of y and z -- This is to account for cubic stuff not working in CQMs
yz = [
    [
        [[Binary(f"yz_{i}_{j}_{n}_{t}") for t in range(T)] for n in range(C + D)]
        for j in range(D)
    ]
    for i in range(C)
]

# Distance matrix
d = [[abs(i - j) for i in range(C + D)] for j in range(C + D)]

cqm = ConstrainedQuadraticModel()

for t in range(T):
    cqm.add_constraint(
        quicksum([x[i][m][t] for i in range(C) for m in range(C + D)]) == C
    )

    cqm.add_constraint(
        quicksum([y[j][n][t] for j in range(D) for n in range(C + D)]) == D
    )

    for n in range(C + D):
        cqm.add_constraint(
            quicksum([x[i][n][t] for i in range(C)] + [y[j][n][t] for j in range(D)])
            == 1
        )

    for j in range(D):
        cqm.add_constraint(quicksum([y[j][n][t] for n in range(C + D)]) == 1)

    for i in range(C):
        cqm.add_constraint(quicksum([x[i][m][t] for m in range(C + D)]) == 1)
        for j in range(D):
            for n in range(C + D):
                cqm.add_constraint(yz[i][j][n][t] - y[j][n][t] <= 0)
                cqm.add_constraint(yz[i][j][n][t] - z[j][i][t] <= 0)
                cqm.add_constraint(yz[i][j][n][t] - y[j][n][t] - z[j][i][t] >= -1)


# C flow
c_flow = 0

for t in range(T):
    for i in range(C):
        for j in range(D):
            for n in range(C + D):
                for m in range(C + D):
                    c_flow += d[m][n] * x[i][m][t] * yz[i][j][n][t]


# C move
c_move = 0

for t in range(T):
    for m in range(C + D):
        for n in range(C + D):
            for i in range(C):
                c_move += d[m][n] * d[m][n] * x[i][m][t] * x[i][n][(t + 1) % T]

            for j in range(D):
                c_move += d[m][n] * d[m][n] * y[j][m][t] * y[j][n][(t + 1) % T]

cqm.set_objective(c_flow + c_move)

sampler = LeapHybridCQMSampler()
sampleset = sampler.sample_cqm(cqm).filter(lambda d: d.is_feasible)
output = sampleset.first.sample
x_out = []

# x
# for t in range(T):
#     for m in range(C + D):
#         x_out.append(int(output[f"x_0_{m}_{t}"]))
#
#     x_out.append("next")

print(x_out)
