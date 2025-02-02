from dwave.system import LeapHybridCQMSampler
from dimod import Binary, ConstrainedQuadraticModel, quicksum
import numpy as np
import matplotlib.pyplot as plt


class QPSolver:
    def __init__(self, A, C, D, x, y) -> None:
        self.lx = x
        self.ly = y

        self.C = C
        self.D = D
        self.T = 6
        self.A = A

        self.x = [
            [[Binary(f"x_{i}_{m}_{t}") for t in range(self.T)] for m in range(x * y)]
            for i in range(self.C)
        ]
        self.y = [
            [[Binary(f"y_{j}_{n}_{t}") for t in range(self.T)] for n in range(x * y)]
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
                (((j % x) - (i % x)) ** 2 + ((j // x) - (i // x)) ** 2) ** 0.5
                for i in range(x * y)
            ]
            for j in range(x * y)
        ]

        self.r = [
            [
                30
                + a * np.cos(2 * np.pi * min([i, j, x - i - 1, y - j - 1]) / min(x, y))
                for j in range(y)
                for i in range(x)
            ]
            for a in [-A, -A / 4, A / 4, A, A / 4, -A / 4]
        ]

        plt.plot(self.r[0])
        plt.plot(self.r[1])
        plt.plot(self.r[2])
        plt.show()

        # print(self.r[0])
        # print(self.r[1])
        # print(self.r[2])

        self.result = None

    def setup_cqm(self):
        # Setup the constraints and the objective function for the self.CQM
        self.cqm = ConstrainedQuadraticModel()

        c_flow = 0
        c_move = 0

        for t in range(self.T):
            for i in range(self.C):
                for j in range(self.D):
                    for n in range(self.lx * self.ly):
                        for m in range(self.lx * self.ly):
                            c_flow += (
                                -self.x[i][m][t]
                                * self.y[j][n][t]
                                * self.r[t][n]
                                / (1 + self.d[m][n])
                            )

                for n in range(self.lx * self.ly):
                    for m in range(self.lx + self.ly):
                        c_move += (
                            self.d[m][n]
                            * self.d[m][n]
                            * self.x[i][m][t]
                            * self.x[i][n][(t + 1) % self.T]
                        )

            for j in range(self.D):
                for m in range(self.lx * self.ly):
                    for n in range(self.lx * self.ly):
                        c_move += (
                            self.d[m][n]
                            * self.d[m][n]
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
                        for m in range(self.lx * self.ly)
                    ]
                )
                == self.C
            )

            self.cqm.add_constraint(
                quicksum(
                    [
                        self.y[j][n][t]
                        for j in range(self.D)
                        for n in range(self.lx * self.ly)
                    ]
                )
                == self.D
            )

            for n in range(self.lx * self.ly):
                self.cqm.add_constraint(
                    quicksum(
                        [self.x[i][n][t] for i in range(self.C)]
                        + [self.y[j][n][t] for j in range(self.D)]
                    )
                    <= 1
                )

            for j in range(self.D):
                self.cqm.add_constraint(
                    quicksum([self.y[j][n][t] for n in range(self.lx * self.ly)]) == 1
                )

            for i in range(self.C):
                self.cqm.add_constraint(
                    quicksum([self.x[i][m][t] for m in range(self.lx * self.ly)]) == 1
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

        data = [
            [[0 for _ in range(self.lx)] for _ in range(self.ly)] for _ in range(self.T)
        ]

        for t in range(self.T):
            for i in range(self.lx * self.ly):
                x = i % self.lx
                y = i // self.lx

                data[t][y][x] = (
                    1
                    if sum(self.result[f"x_{j}_{i}_{t}"] for j in range(self.C)) == 1
                    else 0
                )

                data[t][y][x] = (
                    2
                    if sum(self.result[f"y_{j}_{i}_{t}"] for j in range(self.D)) == 1
                    else data[t][y][x]
                )

        return data

    def create_heatmap(self):
        # Create a scatterplot of heat for the frontend
        r_winter_columns = self.r[0]
        r_summer_columns = self.r[2]
        max_temp = max(r_summer_columns)

        h = []
        for position in range(self.lx*self.ly):
            temp = r_winter_columns[position]
            h.append(temp)
        winter_colors = np.array(h)

        h = []
        for position in range(self.lx*self.ly):
            temp = r_summer_columns[position]
            h.append(temp)
        summer_colors = np.array(h)

        rows = np.repeat(np.arange(self.ly), self.lx)
        columns = np.tile(np.arange(self.lx), self.ly)
        fig, axs = plt.subplots(1, 2, figsize=(10, 4))

        scatter_1 = axs[0].scatter(
            columns,
            rows,
            c=winter_colors,
            cmap="viridis",
            label=f"Winter Temperature Gradient in the Room",
        )
        axs[0].set_title(f"Winter Relative Temperatures, A = {self.A}")
        axs[0].grid(False)
        axs[0].set_xlim(-0.5, self.lx-0.5)
        axs[0].set_ylim(-0.5, self.ly-0.5)

        scatter_2 = axs[1].scatter(
            columns,
            rows,
            c=summer_colors,
            cmap="viridis",
            label=f"Summer Temperature Gradient in the Room",
        )
        axs[1].set_title(f"Summer Relative Temperatures, A = {self.A}")
        axs[1].grid(False)
        axs[1].set_xlim(-0.5, self.lx-0.5)
        axs[1].set_ylim(-0.5, self.ly-0.5)

        plt.colorbar(scatter_1, ax=axs[0])
        plt.colorbar(scatter_2, ax=axs[1])
        plt.show()
        # plt.savefig("static/plot.png")
        plt.close()


qp = QPSolver(15, 5, 20, 6, 7)
# qp.setup_cqm()
# qp.run_cqm()
# qp.get_results()
qp.create_heatmap()
