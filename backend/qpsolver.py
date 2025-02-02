from dwave.system import LeapHybridCQMSampler
from dimod import Binary, ConstrainedQuadraticModel, quicksum
import numpy as np


class QPSolver:
    def __init__(self, A) -> None:
        self.C = 5
        self.D = 15
        self.T = 4

        self.x = [
            [[Binary(f"x_{i}_{m}_{t}") for t in range(self.T)] for m in range(self.C + self.D)]
            for i in range(self.C)
        ]
        self.y = [
            [[Binary(f"y_{j}_{n}_{t}") for t in range(self.T)] for n in range(self.C + self.D)]
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

    def setup_cqm(self):
        # Setup the constraints and the objective function for the self.CQM
        self.cqm = ConstrainedQuadraticModel()

        for t in range(self.T):
            self.cqm.add_constraint(
                quicksum([self.x[i][m][t] for i in range(self.C) for m in range(self.C + self.D)]) == self.C
            )

            self.cqm.add_constraint(
                quicksum([self.y[j][n][t] for j in range(self.D) for n in range(self.C + self.D)]) == self.D
            )

        for n in range(self.C + self.D):
            self.cqm.add_constraint(
                quicksum([self.x[i][n][t] for i in range(self.C)] + [self.y[j][n][t] for j in range(self.D)])
                == 1
            )

        for j in range(self.D):
            self.cqm.add_constraint(quicksum([self.y[j][n][t] for n in range(self.C + self.D)]) == 1)

        for i in range(self.C):
            self.cqm.add_constraint(quicksum([self.x[i][m][t] for m in range(self.C + self.D)]) == 1)
            for j in range(self.D):
                for n in range(self.C + self.D):
                    self.cqm.add_constraint(self.yz[i][j][n][t] - self.y[j][n][t] <= 0)
                    self.cqm.add_constraint(self.yz[i][j][n][t] - self.z[j][i][t] <= 0)
                    self.cqm.add_constraint(self.yz[i][j][n][t] - self.y[j][n][t] - self.z[j][i][t] >= -1)

    def run_cqm(self):
        # Find an optimal solution to the quadratic program
        pass

    def get_results(self):
        # Output self.x and self.y in a way that is easy to work with for the frontend
        pass
