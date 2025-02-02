from dwave.system import LeapHybridCQMSampler
from dimod import Binary, ConstrainedQuadraticModel, quicksum
import numpy as np
import matplotlib.pyplot as plt

C = 5  # Numer of coolers
D = 15  # Number of servers
T = 4  # Number of time steps

A = 7.5  # Amplitude of temperature change

r_winter_columns = np.array(
    [
        [
            30 + A * abs(np.sin(np.pi * (i / 3))) + A * abs(np.sin(np.pi * (j / 4)))
            for i in range(0, 4)
        ]
        for j in range(0, 5)
    ]
).flatten()
r_summer_columns = np.array(
    [
        [
            30 - A * abs(np.sin(np.pi * (i / 3))) - A * abs(np.sin(np.pi * (j / 4)))
            for i in range(0, 4)
        ]
        for j in range(0, 5)
    ]
).flatten()
c_winter_columns = r_winter_columns
c_summer_columns = r_summer_columns

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
d = [
    [
        (((j % 4) - (i % 4)) ** 2 + ((j // 4) - (i // 4)) ** 2) ** 0.5
        for i in range(C + D)
    ]
    for j in range(C + D)
]

A = 3
r_winter_columns = list(
    np.array(
        [
            [
                30 + A * abs(np.sin(np.pi * (i / 3))) + A * abs(np.sin(np.pi * (j / 4)))
                for i in range(0, 4)
            ]
            for j in range(0, 5)
        ]
    ).flatten()
)
r_summer_columns = list(
    np.array(
        [
            [
                30 - A * abs(np.sin(np.pi * (i / 3))) - A * abs(np.sin(np.pi * (j / 4)))
                for i in range(0, 4)
            ]
            for j in range(0, 5)
        ]
    ).flatten()
)

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

# print(x_out)

# Plotting Temp
max_temp = max(r_summer_columns)

h = []
for position in range(21):
    temp = r_winter_columns[position]
    h.append((temp / max_temp) * 100)
winter_colors = np.array(h)

h = []
for position in range(21):
    temp = r_summer_columns[position]
    h.append((temp / max_temp) * 100)
summer_colors = np.array(h)

x = np.array([i for i in range(4)])
y = np.array([j for j in range(5)])
fig, axs = plt.subplots(1, 2, figsize=(10, 4))
axs[0].scatter(
    x,
    y,
    c=winter_colors,
    cmap="viridis",
    label="Winter Temperature Gradient in the Room",
)
axs[0].set_title("Winter Temperature Gradient")
axs[0].grid(True)
axs[0].colorbar()
axs[1].scatter(
    x,
    y,
    c=summer_colors,
    cmap="viridis",
    label="Summer Temperature Gradient in the Room",
)
axs[1].set_title("Summer Temperature Gradient")
axs[1].grid(True)
axs[1].colorbar()
plt.tight_layout()
plt.show()
plt.close()
