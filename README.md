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

## How to use
To use our code, open views.py in visualizer/visualiser. Here, you will see qpsolve = QPSOlve(5 parameters). This first parameter changes the amplitude of the change in termperature across the room, the second changes the number of coolers, the third the number of servers, the fourth the x dimension of the room, and the fifth the y dimension of the room. Once you have set these values, open a terminal and make sure you are in iQuHack-25-QUBO-Crushers\visualizer, then enter py manage.py runserver. This will initialize the function. After a bit of time, you will recieve a message similar to the one below:

Sampling started<br/>
-4654.719561566389<br/>
System check identified no issues (0 silenced).<br/>
February 02, 2025 - 09:44:50<br/>
Django version 5.1.5, using settings 'visualizer.settings'<br/>
Starting development server at http://127.0.0.1:8000/<br/>
Quit the server with CTRL-BREAK.<br/>

Click on the link while pressing Ctrl on your keyboard to open the results page. Here you will see the optimal results of the simulation across a year every other month.

## Future Work

- Extending the model to **multi-floor data centers**.
- Integrating **real-time temperature data** for adaptive optimization.
- Applying the approach to **general supply chain problems**.

## References

1. Koopmans, T. C., & Beckmann, M. (1957). Assignment Problems and the Location of Economic Activities. _Econometrica_.
2. Burkard, R. E., Çela, E., Pardalos, P. M., & Pitsoulis, L. S. (1998). The Quadratic Assignment Problem. _Handbook of Combinatorial Optimization_.

