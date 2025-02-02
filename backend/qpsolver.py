from dwave.system import LeapHybridCQMSampler
from dimod import Binary, ConstrainedQuadraticModel, quicksum
import numpy as np
import matplotlib.pyplot as plt


class QPSolver:
    def __init__(self, A) -> None:
        self.C = 8
        self.D = 34
        self.T = 6

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

        # self.yz = [
        #     [
        #         [
        #             [Binary(f"yz_{i}_{j}_{n}_{t}") for t in range(self.T)]
        #             for n in range(self.C + self.D)
        #         ]
        #         for j in range(self.D)
        #     ]
        #     for i in range(self.C)
        # ]

        self.d = [
            [
                (((j % 6) - (i % 6)) ** 2 + ((j // 6) - (i // 6)) ** 2) ** 0.5
                for i in range(self.C + self.D)
            ]
            for j in range(self.C + self.D)
        ]

        self.r = [
            [
                30 + a * (abs(np.sin(np.pi * i / 5)) + abs(np.sin(np.pi * j / 6)))
                for j in range(7)
                for i in range(6)
            ]
            for a in [-A, -A / 4, A / 4, A, A / 4, -A / 4]
        ]
        print(self.r[0])
        print(self.r[1])
        print(self.r[2])

        self.result = None

    def setup_cqm(self):
        # Setup the constraints and the objective function for the self.CQM
        self.cqm = ConstrainedQuadraticModel()

        c_flow = 0
        c_move = 0

        for t in range(self.T):
            for i in range(self.C):
                for j in range(self.D):
                    for n in range(self.C + self.D):
                        for m in range(self.C + self.D):
                            c_flow += (
                                -self.x[i][m][t]
                                * self.y[j][n][t]
                                * self.r[t][n]
                                / (1 + self.d[m][n])
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
                            * self.y[j][m][t]
                            * self.y[j][n][(t + 1) % self.T]
                        )

        self.cqm.set_objective(c_flow + c_move)

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
                # for j in range(self.D):
                #     for n in range(self.C + self.D):
                #         self.cqm.add_constraint(
                #             self.yz[i][j][n][t] - self.y[j][n][t] <= 0
                #         )
                #         self.cqm.add_constraint(
                #             self.yz[i][j][n][t] - self.z[j][i][t] <= 0
                #         )
                #         self.cqm.add_constraint(
                #             self.yz[i][j][n][t] - self.y[j][n][t] - self.z[j][i][t]
                #             >= -1
                #         )

    def run_cqm(self):
        # Find an optimal solution to the quadratic program
        sampler = LeapHybridCQMSampler()

        print("Sampling started")
        sampleset = sampler.sample_cqm(self.cqm).filter(lambda d: d.is_feasible)
        print(sampleset.first.energy)

        self.result = sampleset.first.sample

    def get_results(self):
        # Output self.x and self.y in a way that is easy to work with for the frontend
        if self.result is None:
            print("Run CQM before getting result")
            return None

        data = [[[0 for _ in range(6)] for _ in range(7)] for _ in range(self.T)]

        for t in range(self.T):
            for i in range(self.C + self.D):
                x = i % 6
                y = i // 6

                data[t][y][x] = (
                    1
                    if sum(self.result[f"x_{j}_{i}_{t}"] for j in range(self.C)) == 1
                    else 2
                )

        return data

    def create_heatmap(self):
        # Create a scatterplot of heat for the frontend
        r_winter_columns = self.r[0]
        r_summer_columns = self.r[2]
        max_temp = max(r_summer_columns)

        h = []
        for position in range(42):
            temp = r_winter_columns[position]
            h.append((temp / max_temp) * 100)
        winter_colors = np.array(h)

        h = []
        for position in range(42):
            temp = r_summer_columns[position]
            h.append((temp / max_temp) * 100)
        summer_colors = np.array(h)

        x = np.repeat(np.arange(7), 6)
        print(x)
        y = np.tile(np.arange(6), 7)
        print(y)
        fig, axs = plt.subplots(1, 2, figsize=(10, 4))
        scatter_1 = axs[0].scatter(
            x,
            y,
            c=winter_colors,
            cmap="viridis",
            label="Winter Temperature Gradient in the Room",
        )
        axs[0].set_title("Winter Temperature Gradient")
        axs[0].grid(False)

        scatter_2 = axs[1].scatter(
            x,
            y,
            c=summer_colors,
            cmap="viridis",
            label="Summer Temperature Gradient in the Room",
        )
        axs[1].set_title("Summer Temperature Gradient")
        axs[1].grid(False)

        plt.colorbar(scatter_1, ax=axs[0])
        plt.colorbar(scatter_2, ax=axs[1])
        plt.show()
        # plt.savefig("static/plot.png")
        plt.close()


# qp = QPSolver(10)
# qp.setup_cqm()
# qp.run_cqm()
# print(qp.get_results())

qpsolver = QPSolver(15)
qpsolver.create_heatmap()
