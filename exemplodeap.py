import random
import numpy
from deap import base
from deap import creator
from deap import algorithms
from deap import tools
import matplotlib.pyplot as plt


# inserindo os produtos

class Produto():
    def __init__(self, nome, espaco, valor):
        self.nome = nome
        self.espaco = espaco
        self.valor = valor
        
lista_produtos = []
lista_produtos.append(Produto("Geladeira Dako", 0.751, 999.90))
lista_produtos.append(Produto("Iphone 6", 0.0000899, 2911.12))
lista_produtos.append(Produto("TV 55' ", 0.400, 4346.99))
lista_produtos.append(Produto("TV 50' ", 0.290, 3999.90))
lista_produtos.append(Produto("TV 42' ", 0.200, 2999.00))
lista_produtos.append(Produto("Notebook Dell", 0.00350, 2499.90))
lista_produtos.append(Produto("Ventilador Panasonic", 0.496, 199.90))
lista_produtos.append(Produto("Microondas Electrolux", 0.0424, 308.66))
lista_produtos.append(Produto("Microondas LG", 0.0544, 429.90))
lista_produtos.append(Produto("Microondas Panasonic", 0.0319, 299.29))
lista_produtos.append(Produto("Geladeira Brastemp", 0.635, 849.00))
lista_produtos.append(Produto("Geladeira Consul", 0.870, 1199.89))
lista_produtos.append(Produto("Notebook Lenovo", 0.498, 1999.90))
lista_produtos.append(Produto("Notebook Asus", 0.527, 3999.00))

espacos = []
valores = []
nomes = []
for produto in lista_produtos:
    espacos.append(produto.espaco)
    valores.append(produto.valor)
    nomes.append(produto.nome)
limite = 3

# implementação do deap

toolbox = base.Toolbox() #função para fazer a inicialização dos recursos da biblioteca.
creator.create("FitnessMax", base.Fitness, weights=(1.0, )) #função de avaliação.
creator.create("Individual", list, fitness=creator.FitnessMax) #criando o individuo.
toolbox.register("attr_bool", random.randint, 0, 1) #registro
toolbox.register("individual", tools.initRepeat, creator.Individual,
                 toolbox.attr_bool, n=len(espacos)) #criação dos individuos.
toolbox.register("population", tools.initRepeat, list, toolbox.individual) #função para a criação da população.

#criando a função de valiação.

def avaliacao(individual):
    nota = 0
    soma_espacos = 0
    for i in range(len(individual)):
       if individual[i] == 1:
           nota += valores[i]
           soma_espacos += espacos[i]
    if soma_espacos > limite:
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
        for i in range(len(lista_produtos)):
            if individuo[i] == 1:
                soma += valores[i]
                print("Nome: %s R$ %s " % (lista_produtos[i].nome,
                                           lista_produtos[i].valor))
        print("Melhor solução: %s" % soma)
        
    valores_grafico = info.select("max")
    plt.plot(valores_grafico)
    plt.title("Acompanhamento dos valores")
    plt.show()