import pandas as pd
import random
import numpy
from deap import base
from deap import creator
from deap import algorithms
from deap import tools
import matplotlib.pyplot as plt

df = pd.read_csv("C:/Users/mathe/Downloads/data.csv")


# implementação do deap

toolbox = base.Toolbox() #função para fazer a inicialização dos recursos da biblioteca.
creator.create("FitnessMax", base.Fitness, weights=(1.0, )) #função de avaliação.
creator.create("Individual", list, fitness=creator.FitnessMax) #criando o individuo.
toolbox.register("attr_bool", random.randint, 0, 1) #registro
toolbox.register("individual", tools.initRepeat, creator.Individual,
                 toolbox.attr_bool, n=len(df)) #criação dos individuos.
toolbox.register("population", tools.initRepeat, list, toolbox.individual) #função para a criação da população.

#criando a função de valiação.

def avaliacao(individual):
    nota = 0
    soma_espacos = 0
    for i in range(len(individual)):
       if individual[i] == 1:
           nota += df[i]
           soma_espacos += df[i]
    if soma_espacos > df:
        nota = 1
    return nota / 100000,

toolbox.register("evaluate", avaliacao) #repassando a função de avalição.
toolbox.register("mate", tools.cxOnePoint) #qual tipo de crossover vaiser utilizado.
toolbox.register("mutate", tools.mutFlipBit, indpb = 0.01) #mudança dos bits, de 0 para 1 e de 1 para 0.
toolbox.register("select", tools.selRoulette) #maneira que vamos selecionar  os individuos para fazer o crossover.

if __name__ == "__main__":
    random.seed(1)
    populacao = toolbox.population(n = 20) #criando a população.
    probabilidade_crossover = 1.0 #probabilidade dele fazer o crossover ou não.
    probabilidade_mutacao = 0.01 #probabilidade dele fazer o mutação ou não.
    numero_geracoes = 100
    
    estatisticas = tools.Statistics(key=lambda individuo: individuo.fitness.values)
    estatisticas.register("max", numpy.max)
    estatisticas.register("min", numpy.min)
    estatisticas.register("med", numpy.mean)
    estatisticas.register("std", numpy.std)
    
    populacao, info = algorithms.eaSimple(populacao, toolbox,
                                          probabilidade_crossover,
                                          probabilidade_mutacao,
                                          numero_geracoes, estatisticas)
    melhores = tools.selBest(populacao, 1)
    for individuo in melhores:
        print(individuo)
        print(individuo.fitness)
        #print(individuo[1])
        soma = 0
        for i in range(len(df)):
            if individuo[i] == 1:
                soma += df[i]
                print("Nome: %s R$ %s " % (df[i].nome,
                                           df[i].valor))
        print("Melhor solução: %s" % soma)
        
        valores_grafico = info.select("max")
        plt.plot(valores_grafico)
        plt.title("Acompanhamento dos valores")
        plt.show()