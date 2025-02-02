from dwave.system import LeapHybridCQMSampler
from dimod import Binary, ConstrainedQuadraticModel, quicksum
import numpy as np


class QPSolver:
    def __init__(self, A) -> None:
        C = 5
        D = 15
        T = 4

        self.cqm = ConstrainedQuadraticModel()
        self.x = [
            [[Binary(f"x_{i}_{m}_{t}") for t in range(T)] for m in range(C + D)]
            for i in range(C)
        ]
        self.y = [
            [[Binary(f"y_{j}_{n}_{t}") for t in range(T)] for n in range(C + D)]
            for j in range(D)
        ]

        self.yz = [
            [
                [
                    [Binary(f"yz_{i}_{j}_{n}_{t}") for t in range(T)]
                    for n in range(C + D)
                ]
                for j in range(D)
            ]
            for i in range(C)
        ]

        self.d = [
            [
                (((j % 4) - (i % 4)) ** 2 + ((j // 4) - (i // 4)) ** 2) ** 0.5
                for i in range(C + D)
            ]
            for j in range(C + D)
        ]

    def setup_cqm(self):
        pass

    def run_cqm(self):
        pass
