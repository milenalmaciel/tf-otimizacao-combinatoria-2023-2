import re
import pyomo.environ as pyo
import time
import numpy as np
import time

model = pyo.ConcreteModel() #instancia o modelo concreto

filename = input()

file = open(str(filename), "r")
first_line = file.readline()
lines = [] #
pattern = r"\b\d+\b" #regex para achar os numeros dentro da string
matches = re.findall(pattern, first_line) #leitura da primeira linha

if(len(matches) >= 2):
    N = int(matches[0]) #colunas
    M = int(matches[1]) #linhas


#leitura do resto das linhas é feita abaixo
while True:
    rest_of_lines = file.readline()
    
    numbers_string = rest_of_lines[1:].strip()
    numbers_string = numbers_string.split()

    numbers = [int(num) for num in numbers_string]

    lines.append(numbers)#lines no final irá conter todos os sets e seus elementos
    if not rest_of_lines:
        break


incidence = np.zeros((M, N), dtype = int) #cria a matriz de incidencia incialmente zerada
    
for subset, row in enumerate(lines):
    for element in row:
        incidence[subset-1][element-1] = 1

#print(incidence) imprime a matriz de incidencia

model.rows = pyo.RangeSet(M-1) #passa para o modelo o tamanho das linhas
model.cols = pyo.RangeSet(N-1) #passa para o modelo o tamanho das colunas
model.x = pyo.Var(model.rows, within = pyo.Binary) #variavel de decisão binaria, garante que a formulação é inteira

#função objetivo é definida aqui
model.obj = pyo.Objective(expr = sum(model.x[j] for j in model.rows), sense = pyo.maximize)


#regra usada na restrição é definida aqui pois a expressão é muito grande
def constraint1(model, j):
    return sum(incidence[i-1][j-1]*model.x[j] for i in model.rows if j-1 < len(incidence[i-1])) <= 1

model.constraint = pyo.Constraint(model.rows, rule = constraint1) #definição da restrição

opt = pyo.SolverFactory("glpk")
start = time.time()# inicio da contagem do tempo
opt.solve(model)
finish = time.time() #fim da contagem do tempo
final_time = finish  - start #calculo do tempo final levado
model.display()#apesar de sempre ser um numero inteiro, o model.display() imprime como um float


print("melhor solução: " + str(int(pyo.value(model.obj))))#imprime o melhor
print(" ")
print("tempo final: " + str(final_time)) #imprime o tempo levado para rodar a otimização

