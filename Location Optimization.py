import gurobipy as gp
import numpy as np
import pandas as pd
from gurobipy import quicksum
from gurobipy import GRB,Model
import math

from scipy.stats import uniform

def distancepolar(r1, r2, theta1, theta2,calc):
    return np.sqrt(r1**2 + r2**2 - 2*r1*r2*calc)

def calculateDistance(x1,y1,x2,y2):
    dist = ((x2 - x1)*(x2 - x1) + (y2 - y1)*(y2-y1))
    return dist

# Create the model
m = Model('Baseball')

# Set parameters
m.setParam('OutputFlag', True)

V = [1 for i in range(4)]
a = 5  #Radius Length to First Base
b = 10
y = 25 #Whole Radius
B =[(a,0),(a,a),(0,a)]
P = [1,.5,.5,.5]
Alpha = 10 
Beta = 5
Gamma = [2.5,2.5,2.5]
H = 4

n = 10000
start = 0
width = 25
R_data_uniform = uniform.rvs(size=n, loc = start, scale=width)
n = 10000
start = 0
width = (math.pi)/2
Theta_data_uniform = uniform.rvs(size=n, loc = start, scale=width)

pos = [(R_data_uniform[i]*math.cos(Theta_data_uniform[i]),R_data_uniform[i]*math.sin(Theta_data_uniform[i])) for i in range(n)]

#Add Variables
X = m.addVars(3,name ='X')
Y = m.addVars(3,name = 'Y')
X4 = m.addVar((1),name = 'Player-4 X')
Y4 = m.addVar((1),name = 'P4 Y')
DT1 = m.addVars(n,name = 'X1Time from Distance to Ball')
DT2 = m.addVars(n,name = 'Time from Distance to Ball')
DT3 = m.addVars(n,name = 'Time from Distance to Ball')
DT4 = m.addVars(n,name = 'Time from Distance to Ball')
TM = m.addVars(n,name = 'Minimum Time')
#TS1 = m.addVars(n, name = 'Throw Time to Each Base 1')
#TS2 = m.addVars(n, name = 'Throw Time to Each Base 2')
#TS3 = m.addVars(n, name = 'Throw Time to Each Base 3')
#TS4 = m.addVars(n, name = 'Throw Time to Each Base 4')
#calc = m.addVars(n,name='temp')
#AvgHT1 = m.addVars((1),name = 'Average Throw Time 1')
#AvgHT2 = m.addVars((1),name = 'Average Throw Time 1')
#AvgHT3 = m.addVars((1),name = 'Average Throw Time 1')
#AvgHT4 = m.addVars((1),name = 'Average Throw Time 1')

#Add Constraints
m.addConstrs((calculateDistance(X[i],0,Y[i],0) >= b for i in range(3)), name = 'Outfield min constr')
m.addConstrs((calculateDistance(X[i],0,Y[i],0) <= y for i in range(3)), name = 'Outfield max constr')
m.addConstr(calculateDistance(X4,0,Y4,0) <= y, name = 'Infield max constr')


m.addConstrs(DT1[i] == calculateDistance(X[0],pos[i][0],pos[i][1],Y[0])/V[0] for i in range(n))
m.addConstrs(DT2[i] == calculateDistance(X[1],pos[i][0],pos[i][1],Y[1])/V[0] for i in range(n))
m.addConstrs(DT3[i] == calculateDistance(X[2],pos[i][0],pos[i][1],Y[2])/V[0] for i in range(n))
m.addConstrs(DT4[i] == calculateDistance(X4,pos[i][0],pos[i][1],Y4)/V[0] for i in range(n))
m.addConstrs((TM[i] == gp.min_([DT1[i],DT2[i],DT3[i],DT4[i]]) for i in range(n)),"min_constraints")

m.setObjective(gp.quicksum(TM[i] for i in range(n)),GRB.MINIMIZE)
m.optimize()

status_code = {1:'LOADED', 2:'OPTIMAL', 3:'INFEASIBLE', 4:'INF_OR_UNBD', 5:'UNBOUNDED'}
status = m.status

print('The optimization status is {}' .format(status_code[status]))

m.printStats()