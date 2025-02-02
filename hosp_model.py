import numpy as np
import dimod
import random
from dwave.optimization.model import Model
from dwave.system import LeapHybridNLSampler
from dwave.system import DWaveSampler

def main():
    
    ## Trial
    N = 10
    T = 5
    C = 3
    D = 4
    closets = np.zeros((C, T)) # C = 3, so size = 15
    for j in range(T):
        for i in range(C):
            closets[i][j] = (T+C-i)
            
    depts = np.zeros((D, T)) # D = 4, so size = 20
    for i in range(C):
        depts[i][0] = 1
    for j in range(T):
        for i in range(C):
            closets[i][j] = T+C-i
    for i in range(C):
        depts[i][T-1] = 1

    # Distance Matrix
    d = np.zeros((N,N))
    for i in range(N):
        for j in range(N):
            d[i][j] = np.abs(i - j)

    hosp_model_NL(N, T, closets, depts, d)

def hosp_model_NL(N, T, closets, depts, d):

    ## Create the model
    hosp_model = Model()

    ## Create constants 
    # C = int(len(closets)/T)
    # D = int(len(depts)/T)

    C = hosp_model.constant("C")
    D = hosp_model.constant("D")

    ## Declare binary variables
    x = hosp_model.binary((N, N, T))
    y = hosp_model.binary((N, N, T))
    z = hosp_model.binary((N, N, T))

    ## Add constraints

    # Supplies going out from Closet j at time t
    for t in range(T):
        for j in range(C):
            z_sum = 0 
            for i in range(D):
                z_sum += z[j][i][t]
            Model.add_constraint(z_sum == closets[j][t])

    
    # Supplies going out from Closet j at time t
    for t in range(T):
        for i in range(D):
            z_sum = 0 
            for j in range(C):
                z_sum += z[j][i][t]
            Model.add_constraint(z_sum == closets[j][t])

    # Number of departments = D same at each time t
    for t in range(T):
        # num_depts = 0
        # for i in range(D):
        #     for m in range(N):
        #         num_depts += x[i][m][t]
        # hosp_model.add_constraint(num_depts == D)
        hosp_model.add_constraint(x.sum() <= D)
            
    # Number of closet = C at each time t
    for t in range(T):
        num_closets = 0
        for j in range(C):
            for m in range(N):
                num_depts += y[j][m][t]
        hosp_model.add_constraint(num_closets == C)

    # No room is both a closet and department at any time t
    for t in range(T):
        for n in range(N):
            sum_x_and_y = 0
            for i in range(D):
                for j in range(C):
                    sum_x_and_y += x[i][n][t] + y[j][n][t]
            hosp_model.add_constraint(sum_x_and_y == 1)

    # Defining the objective function

    # Defining C_move
    C_move = 0
    for t in range(T):
        for i in range(D):
            for m in range(N):
                for n in range(N):
                    C_move += (d[m][n]**2)*(x[i][m][t])*(x[i][n][t]) 

    for t in range(T):
        for j in range(C):
            for m in range(N):
                for n in range(N):
                    C_move += (d[m][n]**2)*(y[j][m][t])*(y[j][n][t]) 

    # Defining C_flow
    C_flow = 0
    for t in range(T):
        for j in range(C):
            for i in range(N):
                for n in range(N):
                    for m in range(N):
                        (d[m][n])*(x[i][m][t])*(y[i][n][t])*(z[j][i][t])

    C_tot = C_move + C_flow

    # Minimizing the objective function
    hosp_model.minimize(C_tot)

    sampler = LeapHybridNLSampler()
    sampler.sample(hosp_model time_limit=15)

if __name__ == '__main__':
    main()