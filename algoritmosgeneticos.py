from random import random
import matplotlib.pyplot as plt
import pymysql

#criando a classe dos produtos que serão adicionados.
class Produto():
    def __init__(self, nome, espaco, valor):
        self.nome = nome 
        self.espaco = espaco 
        self.valor = valor 
        
#criando a classe dos induviduos que farão parte das evoluções, obs: claase que vai armazenar o individuo.
class individuo():
    def __init__(self, espacos, valores, limite_espacos, geracao=0):
        self.espacos = espacos
        self.valores = valores
        self.limite_espacos = limite_espacos
        self.nota_avaliacao = 0
        self.espaco_usado = 0
        self.geracao = geracao
        self.cromossomo = []
        
        for i in range(len(espacos)):
            if random() < 0.5:
                self.cromossomo.append("0")
            else:
                self.cromossomo.append("1")
                
# criando uma avaliação para a validade de cada produto no transporte.
    def avaliacao(self):
        nota = 0
        soma_espacos = 0
        for i in range(len(self.cromossomo)):
            if self.cromossomo[i] == '1':
                nota += self.valores[i]
                soma_espacos += self.espacos[i]
        if soma_espacos > self.limite_espacos:
            nota = 1
        self.nota_avaliacao = nota
        self.espaco_usado = soma_espacos
        
# criando uma função para fazer o crossover/reprodução entre as combinações
    def crossover(self, outro_individuo):
        corte = round(random() * len(self.cromossomo))
        
        filho1 = outro_individuo.cromossomo[0:corte] + self.cromossomo[corte::]
        filho2 = self.cromossomo[0:corte] + self.cromossomo[corte::]
        
        filhos = [individuo(self.espacos, self.valores, self.limite_espacos, self.geracao + 1),
                  individuo(self.espacos, self.valores, self.limite_espacos, self.geracao + 1)]
        filhos[0].cromossomo = filho1
        filhos[1].cromossomo = filho2
        return filhos
            
# realizando mutação nos elementos
    def mutacao(self, taxa_mutacao):
        print("Antes %s" % self.cromossomo)
        for i in range(len(self.cromossomo)):
            if random() < taxa_mutacao:
                if self.cromossomo[i] == '1':
                    self.cromossomo[i] = '0'
                else:
                    self.cromossomo[i] = '1'
        return self
    
# criando uma classe para armazenar todas as informações e gerar os resultaods ligados ao algoritimo genetico.
class AlgoritmoGenetico():
    def __init__(self, tamanho_populacao):
        self.tamanho_populacao = tamanho_populacao
        self.populacao = []
        self.geracao = 0
        self.melhor_solucao = 0
        self.lista_solucoes = []
        
    def inicializa_populacao(self, espacos, valores, limite_espacos):
        for i in range(self.tamanho_populacao):
            self.populacao.append(individuo(espacos, valores, limite_espacos))
        self.melhor_solucao = self.populacao[0]
        
#avaliação da população
    def ordena_populacao(self):
        self.populacao = sorted(self.populacao,
                                key = lambda populacao: populacao.nota_avaliacao,
                                reverse = True)
        
#melhor individuo
    def melhor_individuo(self, individuo):
        if individuo.nota_avaliacao > self.melhor_solucao.nota_avaliacao:
            self.melhor_solucao = individuo
        
#soma das avaliacoes
    def soma_avaliacoes(self):
        soma = 0
        for individuo in self.populacao:
            soma += individuo.nota_avaliacao
        return soma
    
#retornar o id do individuo que foi selecionado.
    def seleciona_pai(self, soma_avaliacao):
        pai = -1
        valor_sorteado = random() * soma_avaliacao
        soma = 0
        i = 0
        while i < len(self.populacao) and soma <valor_sorteado:
            soma += self.populacao[i].nota_avaliacao
            pai += 1
            i += 1
        return pai
        
# função para visualizar as melhores condições.
    def visualiza_geracao(self):
        melhor = self.populacao[0]
        print("G:%s -> Valor: %s Espaço: %s Cromossomo: %s" % (self.populacao[0].geracao,
                                                               melhor.nota_avaliacao,
                                                               melhor.espaco_usado,
                                                               melhor.cromossomo))
        
# fazendo a resolução de tudo.
    def resolver(self, taxa_mutacao, numero_geracoes, espacos, valores, limite_espacos):
        self.inicializa_populacao(espacos, valores, limite_espacos)
        
        for individuo in self.populacao:
            individuo.avaliacao()
        
        self.ordena_populacao()
        self.melhor_solucao = self.populacao[0]
        self.lista_solucoes.append(self.melhor_solucao.nota_avaliacao)
        
        self.visualiza_geracao()
        
        for geracao in range(numero_geracoes):
            soma_avaliacao = self.soma_avaliacoes()
            nova_populacao = []
            
            for individuos_gerados in range(0, self.tamanho_populacao, 2):
                pai1 = self.seleciona_pai(soma_avaliacao)
                pai2 = self.seleciona_pai(soma_avaliacao)
                
                filhos = self.populacao[pai1].crossover(self.populacao[pai2])
                
                nova_populacao.append(filhos[0].mutacao(taxa_mutacao))
                nova_populacao.append(filhos[1].mutacao(taxa_mutacao))
            
            self.populacao = list(nova_populacao)
            
            for individuo in self.populacao:
                individuo.avaliacao()
            
            self.ordena_populacao()
            
            self.visualiza_geracao()
            
            melhor = self.populacao[0]
            self.lista_solucoes.append(melhor.nota_avaliacao)
            self.melhor_individuo(melhor)
        
        print("\nMelhor solução -> G: %s Valor: %s Espaço: %s Cromossomo: %s" %
              (self.melhor_solucao.geracao,
               self.melhor_solucao.nota_avaliacao,
               self.melhor_solucao.espaco_usado,
               self.melhor_solucao.cromossomo))
        
        return self.melhor_solucao.cromossomo
    
#inserindo os produtos na lista com my sql.
if __name__ == '__main__':
    #p1 = Produto("Iphone 6", 0.0000899, 2199,12)
    lista_produtos = []
    conexao = pymysql.connect(host='localhost', user='root', passwd='narutogara', db='produtos')
    cursor = conexao.cursor()
    cursor.execute('select nome, espaco, valor, quantidade from produtos')
    for produto in cursor:
        #print(produto[3])
        for i in range(produto[3]):
            lista_produtos.append(Produto(produto[0], produto[1], produto[2]))
                
    cursor.close()
    conexao.close()
    
    
    
#inserindo os produtos na lista.   
    '''lista_produtos.append(Produto("Geladeira Dako", 0.751, 999.90))
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
    lista_produtos.append(Produto("Notebook Asus", 0.527, 3999.00))'''
    #for produto in lista_produtos:
    #    print(produto.nome)
    
    espacos = []
    valores = []
    nomes = []
    for produto in lista_produtos:
        espacos.append(produto.espaco)
        valores.append(produto.valor)
        nomes.append(produto.nome)
    limite = 10
    tamanho_populacao = 20
    taxa_mutacao = 0.01
    numero_geracoes = 100
    ag = AlgoritmoGenetico(tamanho_populacao)
    resultado = ag.resolver(taxa_mutacao, numero_geracoes, espacos, valores, limite)
    for i in range(len(lista_produtos)):
        if resultado[i] == '1':
            print("Nome: %s R$ %s " % (lista_produtos[i].nome,
                                       lista_produtos[i].valor))
            
    
    #for valor in ag.lista_solucoes:
    #    print(valor)
    plt.plot(ag.lista_solucoes)
    plt.title("Acompanhamento dos valores")
    plt.show() 
    

#%% treino para entender melhor
# tem que se criar mais de um individuo para fazer o crossover/reprodução.
    
    individuo1 = individuo(espacos, valores, limite)
    print("\nindividuo 1")
    for i in range(len(lista_produtos)):
        if individuo1.cromossomo[i] == '1':
            print ("Nome: %s R$ %s" % (lista_produtos[i].nome, lista_produtos[i].valor))
            
    individuo1.avaliacao()
    print("Nota = %s" % individuo1.nota_avaliacao)
    print("Espaços usados = %s" % individuo1.espaco_usado)
    
            
    individuo2 = individuo(espacos, valores, limite)
    print("\nindividuo 2")
    for i in range(len(lista_produtos)):
        if individuo1.cromossomo[i] == '1':
            print ("Nome: %s R$ %s" % (lista_produtos[i].nome, lista_produtos[i].valor))
            
    individuo2.avaliacao()
    print("Nota = %s" % individuo2.nota_avaliacao)
    print("Espacos usados = %s" % individuo2.espaco_usado)

#testando o crossover
    individuo1.crossover(individuo2)

#testando a mutação
    individuo1.mutacao(0.05)
    individuo2.mutacao(0.05)

#gerando o algoritmo genetico
    ag.inicializa_populacao(espacos, valores, limite)
    for individuo in ag.populacao:
        individuo.avaliacao()
    ag.ordena_populacao()
    ag.melhor_individuo(ag.populacao[0])
    for i in range(ag.tamanho_populacao):
        print("*** Indivídu %s ****\n" % str(ag.populacao[i].espacos),
              "Valores = %s\n" % str(ag.populacao[i].valores),
              "Cromossomo = %s\n" % str(ag.populacao[i].cromossomo),
              "Nota = %s\n" % ag.populacao[i].nota_avaliacao)  

# melhor solução para o problema
    print("Melhor solução para o problema: %s" % ag.melhor_solucao.cromossomo,
          "Nota = %s\n" % ag.melhor_solucao.nota_avaliacao)

#soma das avaliações
    soma = ag.soma_avaliacoese()
    print("Soma das avaliações: %s" % soma)

#gerando uma nova populacao com crossover
    nova_populacao = []
    probabilidade_mutacao = 0.01
    for individuos_gerados in range(0, ag.tamanho_populacao, 2):
        pai1 = ag.seleciona_pai(soma)
        pai2 = ag.seleciona_pai(soma)
                   
        filhos = ag.populacao[pai1].crossover(ag.populacao[pai2])
        nova_populacao.append(filhos[0].mutacao(probablidade_mutacao))
        nova_populacao.append(filhos[1].mutacao(probablidade_mutacao))
        
    ag.populacao = list(nova_populacao)
    for individuo in ag.populacao:
        individuo.avalicao()
    ag.ordema_populacao()
    ag.melhor_individuo(ag.populacao[0])
    soma = ag.soma_avaliacoes()
    
    print("Melhor: %s" % ag.melhor_solucao.cromossomo, "Valor: %s\n" % ag.melhor_solucao.nota_avaliacao)
