import numpy as np
import json

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
).flatten().tolist()

r_summer_columns = np.array(
    [
        [
            30 - A * abs(np.sin(np.pi * (i / 3))) - A * abs(np.sin(np.pi * (j / 4)))
            for i in range(0, 4)
        ]
        for j in range(0, 5)
    ]
).flatten().tolist()
c_winter_columns = r_winter_columns
c_summer_columns = r_summer_columns

data = {'C':5, 'D':15, 'T':4, 'A':7, 'r_winter_columns': r_summer_columns, 'r_summer_columns': r_summer_columns, 'c_winter_columns':c_winter_columns, 'c_summer_columns':c_summer_columns }

with open("input_data.json", "w") as outfile: 
    json.dump(data, outfile)

