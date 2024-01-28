import re
import pyomo.environ as pyo
import time
import numpy as np

model = pyo.ConcreteModel() #instancia o modelo concreto

filename = input()

file = open(str(filename), "r")
first_line = file.readline()
lines = [] #
pattern = r"\b\d+\b" #regex para achar os numeros dentro da string
matches = re.findall(pattern, first_line)

if(len(matches) >= 2):
    N = int(matches[0]) #colunas
    M = int(matches[1]) #linhas


while True:
    rest_of_lines = file.readline()
    #print(rest_of_lines + "\n")
    numbers_string = rest_of_lines[1:].strip()
    numbers_string = numbers_string.split()

    numbers = [int(num) for num in numbers_string]
    #time.sleep(2)
    lines.append(numbers)
    if not rest_of_lines:
        break


incidence = np.zeros((M, N), dtype = int) #cria a matrix de incidencia incialmente zerada
    
for subset, row in enumerate(lines):
    for element in row:
        incidence[subset-1][element-1] = 1


#model.incidence = pyo.var([0,M-1], [0, N-1], domain = pyo.Binary) 
model.rows = pyo.RangeSet(M-1)
model.cols = pyo.RangeSet(N-1)
model.is_in_solution = pyo.Var(model.rows, domain = pyo.Binary) #declara a variavel que verifica se o conjunto faz parte da solução ou não

def obj_rule(model):
    return sum(model.is_in_solution[i] for i in model.rows)

model.obj = pyo.Objective(rule = obj_rule, sense = pyo.maximize)



def constraint_rule1(model, i, j):
    somatorio = 0
    for i in model.rows:
        for j in model.cols:
            somatorio += incidence[i][j]*model.is_in_solution[i]
    return somatorio <= 1

model.Constraint1 = pyo.Constraint(model.rows, model.cols, rule = constraint_rule1)

opt = pyo.SolverFactory("glpk")
opt.solve(model)
model.display()
