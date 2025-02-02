from dwave.system import LeapHybridCQMSampler
from dimod import Binary, ConstrainedQuadraticModel, quicksum
import numpy as np
import matplotlib.pyplot as plt


class QPSolver:
    def __init__(self, A) -> None:
        self.C = 5
        self.D = 15
        self.T = 4

        self.x = [
            [
                [Binary(f"x_{i}_{m}_{t}") for t in range(self.T)]
                for m in range(self.C + self.D)
            ]
            for i in range(self.C)
        ]
        self.y = [
            [
                [Binary(f"y_{j}_{n}_{t}") for t in range(self.T)]
                for n in range(self.C + self.D)
            ]
            for j in range(self.D)
        ]

        self.z = [
            [[Binary(f"z_{j}_{i}_{t}") for t in range(self.T)] for i in range(self.C)]
            for j in range(self.D)
        ]

        self.yz = [
            [
                [
                    [Binary(f"yz_{i}_{j}_{n}_{t}") for t in range(self.T)]
                    for n in range(self.C + self.D)
                ]
                for j in range(self.D)
            ]
            for i in range(self.C)
        ]

        self.d = [
            [
                (((j % 4) - (i % 4)) ** 2 + ((j // 4) - (i // 4)) ** 2) ** 0.5
                for i in range(self.C + self.D)
            ]
            for j in range(self.C + self.D)
        ]

        self.r = [
            [
                [
                    30 + a * (np.sin(np.pi * i / 3) + np.sin(np.pi * j / 4))
                    for j in range(5)
                ]
                for i in range(4)
            ]
            for a in [-A, 0, A, 0]
        ]

        self.result = None

    def setup_cqm(self):
        # Setup the constraints and the objective function for the self.CQM
        self.cqm = ConstrainedQuadraticModel()

        for t in range(self.T):
            self.cqm.add_constraint(
                quicksum(
                    [
                        self.x[i][m][t]
                        for i in range(self.C)
                        for m in range(self.C + self.D)
                    ]
                )
                == self.C
            )

            self.cqm.add_constraint(
                quicksum(
                    [
                        self.y[j][n][t]
                        for j in range(self.D)
                        for n in range(self.C + self.D)
                    ]
                )
                == self.D
            )

            for n in range(self.C + self.D):
                self.cqm.add_constraint(
                    quicksum(
                        [self.x[i][n][t] for i in range(self.C)]
                        + [self.y[j][n][t] for j in range(self.D)]
                    )
                    == 1
                )

            for j in range(self.D):
                self.cqm.add_constraint(
                    quicksum([self.y[j][n][t] for n in range(self.C + self.D)]) == 1
                )

            for i in range(self.C):
                self.cqm.add_constraint(
                    quicksum([self.x[i][m][t] for m in range(self.C + self.D)]) == 1
                )
                for j in range(self.D):
                    for n in range(self.C + self.D):
                        self.cqm.add_constraint(
                            self.yz[i][j][n][t] - self.y[j][n][t] <= 0
                        )
                        self.cqm.add_constraint(
                            self.yz[i][j][n][t] - self.z[j][i][t] <= 0
                        )
                        self.cqm.add_constraint(
                            self.yz[i][j][n][t] - self.y[j][n][t] - self.z[j][i][t]
                            >= -1
                        )

        c_flow = 0
        c_move = 0

        for t in range(self.T):
            for i in range(self.C):
                for j in range(self.D):
                    for n in range(self.C + self.D):
                        for m in range(self.C + self.D):
                            c_flow += (
                                self.d[m][n] * self.x[i][m][t] * self.yz[i][j][n][t]
                            )

                for n in range(self.C + self.D):
                    for m in range(self.C + self.D):
                        c_move += (
                            self.d[m][n]
                            * self.d[m][n]
                            * self.x[i][m][t]
                            * self.x[i][n][(t + 1) % self.T]
                        )

            for j in range(self.D):
                for m in range(self.C + self.D):
                    for n in range(self.C + self.D):
                        c_move += (
                            self.d[m][n]
                            * self.d[m][n]
                            * self.y[j][m][t]
                            * self.y[j][n][(t + 1) % self.T]
                        )

        self.cqm.set_objective(c_flow + c_move)

    def run_cqm(self):
        # Find an optimal solution to the quadratic program
        sampler = LeapHybridCQMSampler()
        sampleset = sampler.sample_cqm(self.cqm).filter(lambda d: d.is_feasible)

        self.result = sampleset.first.sample

    def get_results(self):
        # Output self.x and self.y in a way that is easy to work with for the frontend
        pass

    def create_heatmap(self):
        # Create a scatterplot of heat for the frontend
        h = []
        max_temp = max(self.r_summer_columns)
        r_winter_columns = self.r[0:20]
        r_spring_columns = self.r[20:40]
        r_summer_columns = self.r[40:60]
        r_fall_columns = self.r[60:80]
        for position in range(16):
            temp = r_winter_columns[position]
            h.append(temp/max_temp * 100)
        winter_colors = np.array(h)
        h=[]
        for position in range(16):
            temp = r_summer_columns[position]
            h.append(temp/max_temp * 100)
        summer_colors = np.array(h)

        x = np.array([i for i in range(4)])
        y = np.array([j for j in range(5)])
        fig, axs = plt.subplots(1, 2, figsize=(10, 4))
        axs[0].scatter(x, y, c=winter_colors, cmap="viridis", label="Winter Temperature Gradient in the Room")
        axs[0].set_title("Winter Temperature Gradient")
        axs[0].grid(True)
        axs[0].colorbar()

        axs[1].scatter(x, y, c=summer_colors, cmap="viridis", label="Summer Temperature Gradient in the Room")
        axs[1].set_title("Summer Temperature Gradient")
        axs[1].grid(True)
        axs[1].colorbar()

        plt.tight_layout()
        plt.savefig("static/plot.png")
        plt.close()
