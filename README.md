# QUBO-Crushers D-Wave In Person Submission - iQuHACK 2025

## Overview

This project tackles a modified version of the Quadratic Assignment Problem (QAP), leveraging D-Wave's quantum-hybrid solvers to optimize server and cooling rack placements in a data center. The goal is to minimize energy costs and maximize cooling efficiency by adjusting placements dynamically based on seasonal temperature variations.

## Background

The classic QAP involves assigning **N** facilities to **N** locations while minimizing transport costs based on two factors:

- **Flow matrix (f_jk):** Represents the interaction between facilities.
- **Distance matrix (d_mn):** Represents the physical distance between locations.

In this project, we introduce **time-dependent constraints** and **movement costs**, making the problem more complex and realistic. We aim to optimize placement strategies across multiple time steps, reducing unnecessary movement while ensuring optimal cooling and performance.

## Problem Statement

### Data Center Scenario

Data centers experience varying cooling efficiency based on seasonal temperature changes. For example:

- **Winter:** Racks near windows/outer walls tend to be colder.
- **Summer:** The same locations tend to be hotter.

We model the problem as follows:

- **Servers and cooling racks** are assigned to specific locations within the data center.
- **Cooling efficiency changes seasonally**, affecting the effectiveness of different placements.
- **Relocating racks and servers incurs a cost**, which we set proportinal to the distance moved squared.
- **The goal is to minimize total energy consumption and movement costs** while ensuring that all server loads are managed efficiently.

## Optimization Approach

Using D-Wave’s CQM hybrid solver, we:

1. **Fix the distance matrix (d_mn)** representing rack locations within the data center.
2. **Allow the flow matrix (f_jk) to vary over time**, reflecting seasonal cooling changes.
3. **Introduce a cost function for movement**, penalizing excessive relocation.
4. **Solve the optimization problem** iteratively across multiple time steps to find the best assignment strategy.

## Expected Outcomes

- **Energy savings** by placing high-load servers in naturally cooler areas.
- **Reduced movement costs** by minimizing unnecessary relocation.
- **Scalability analysis** to understand solver performance on larger problem instances.

## Future Work

- Extending the model to **multi-floor data centers**.
- Integrating **real-time temperature data** for adaptive optimization.
- Applying the approach to **general supply chain problems**.

## References

1. Koopmans, T. C., & Beckmann, M. (1957). Assignment Problems and the Location of Economic Activities. _Econometrica_.
2. Burkard, R. E., Çela, E., Pardalos, P. M., & Pitsoulis, L. S. (1998). The Quadratic Assignment Problem. _Handbook of Combinatorial Optimization_.

