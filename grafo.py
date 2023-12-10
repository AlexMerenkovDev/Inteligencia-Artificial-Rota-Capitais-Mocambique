
# %% Estados
class Estado:
    def __init__(self, nome, accoes):
        self.nome = nome
        self.accoes = accoes

    def __str__(self):
        return self.nome


# %% Via - que sao as accoes que os estados podem ter
class Accao:
    def __init__(self, nome, cidade1=None, cidade2=None, distancia=None, caracteristicas=None):
        self.nome = nome
        self.cidade1 = cidade1
        self.cidade2 = cidade2
        self.distancia = distancia
        self.caracteristicas = caracteristicas


    def __str__(self):
        return self.nome

# %% Caracteristicas da Via(accao)
class Caracteristicas:
    def __init__(self, piso, portagem, velocidade_media):
        self.piso = piso
        self.portagem = portagem
        self.velocidade_media = velocidade_media


    def __str__(self):
        return 'Piso: {0}, Portagem: {1}, vel_media: {2}'.format(self.piso, self.portagem,
                                                                self.velocidade_media)

# %% Problema
class Problema:
    def __init__(self, estado_inicial, estados_objectivos, accoes, piso_min, distancias, duracao, custos
                 , escolha):
        self.estado_inicial = estado_inicial
        self.estados_objectivos = estados_objectivos
        self.accoes = accoes
        self.distancias = distancias
        self.duracao = duracao
        self.custos = custos
        self.piso_min = piso_min
        self.escolha = escolha
        self.infinito = 99999

        if not self.distancias:
            self.distancias = {}
            for estado in self.accoes.keys():
                self.distancias[estado] = {}
                for accao in self.accoes[estado].keys():
                    self.distancias[estado][accao] = 1
        if not self.duracao:
            self.duracao = {}
            for estado in self.accoes.keys():
                self.duracao[estado] = {}
                for accao in self.accoes[estado].keys():
                    self.duracao[estado][accao] = 0
        if not self.custos:
            self.custos = {}
            for estado in self.accoes.keys():
                self.custos[estado] = {}
                for accao in self.accoes[estado].keys():
                    self.custos[estado][accao] = 0

    def __str__(self):
        msg = 'Estado inicial: {0} -> Objectivos: {1}'
        return msg.format(self.estado_inicial.nome,
                          self.estados_objectivos.nome)

    def e_objectivo(self, estado):
        return estado in self.estados_objectivos

    def resultado(self, estado, accao):
        if estado.nome not in self.accoes.keys():
            return None
        accoes_estado = self.accoes[estado.nome]
        if accao.nome not in accoes_estado.keys():
            return None
        return accoes_estado[accao.nome]

    def custo_accao(self, estado, accao):
        if estado.nome not in self.custos.keys():
            return self.infinito
        costes_estado = self.custos[estado.nome]
        if accao.nome not in costes_estado.keys():
            return self.infinito
        return costes_estado[accao.nome]

    def distancia_accao(self, estado, accao):
        if estado.nome not in self.distancias.keys():
            return self.infinito
        distancias_estado = self.distancias[estado.nome]
        if accao.nome not in distancias_estado.keys():
            return self.infinito
        return distancias_estado[accao.nome]

    def duracao_accao(self, estado, accao):
        if estado.nome not in self.duracao.keys():
            return self.infinito
        duracao_estado = self.duracao[estado.nome]
        if accao.nome not in duracao_estado.keys():
            return self.infinito
        return duracao_estado[accao.nome]

    def custo_caminho(self, no):
        total = 0
        while no.pai:
            total += self.custo_accao(no.pai.estado, no.accao)
            no = no.pai
        return total

    def distancia_caminho(self, no):
        total = 0
        while no.pai:
            total += self.distancia_accao(no.pai.estado, no.accao)
            no = no.pai
        return total

    def duracao_caminho(self, no):
        total = 0
        while no.pai:
            total += self.duracao_accao(no.pai.estado, no.accao)
            no = no.pai
        return total


# %% No
class No:
    def __init__(self, estado, accao=None, accoes=None, pai=None):
        self.estado = estado
        self.accao = accao
        self.accoes = accoes
        self.pai = pai
        self.filhos = []
        self.custo = 0
        self.distancia = 0
        self.duracao = 0

    def __str__(self):
        return self.estado.nome

    def expandir(self, problema):
        self.filhos = []
        if not self.accoes :
            if self.estado.nome not in problema.accoes.keys():
                return self.filhos
            self.accoes = problema.accoes[self.estado.nome]
        for accao in self.accoes.keys():
            accao_filho = Accao(accao)
            novo_estado = problema.resultado(self.estado, accao_filho)
            accoes_novo = {}
            if novo_estado.nome in problema.accoes.keys():
                accoes_novo = problema.accoes[novo_estado.nome]
            filho = No(novo_estado, accao_filho, accoes_novo, self)
            custo = self.pai.custo if self.pai else 0
            custo += problema.custo_accao(self.estado, accao_filho)
            filho.custo = custo

            distancia = self.pai.distancia if self.pai else 0
            distancia += problema.distancia_accao(self.estado, accao_filho)
            filho.distancia = distancia

            duracao = self.pai.duracao if self.pai else 0
            duracao += problema.duracao_accao(self.estado, accao_filho)
            filho.duracao = duracao
            self.filhos.append(filho)
        return self.filhos

    def filho_melhor(self, problema):
        if not self.filhos:
            return None
        melhor = self.filhos[0]
        for filho in self.filhos:
            for objectivo in problema.estados_objectivos:
                custo_caminho_filho = problema.custo_caminho(filho)
                custo_caminho_melhor = problema.custo_caminho(melhor)
                if (custo_caminho_filho < custo_caminho_melhor):
                    melhor = filho
        return melhor

# %% Definicoes
'''
if  __name__ == '__main':
    accN = Accao('norte')

    accS = Accao('sur')

    accE = Accao('este')

    accO = Accao('oeste')

    coruna = Estado('A Coruña', [accS, accE])
    bilbao = Estado('Bilbao', [accS, accE, accO])
    barcelona = Estado('Barcelona', [accS, accO])
    lisboa = Estado('Lisboa', [accN, accS, accE])
    madrid = Estado('Madrid', [accN, accS, accE, accO])
    valencia = Estado('Valencia', [accN, accS, accO])
    faro = Estado('Faro', [accN, accE])
    sevilla = Estado('Sevilla', [accN, accE, accO])
    granada = Estado('Granada',[accN,accO])

    viagens = {'A Coruña': {'sul': lisboa,
                        'este': bilbao},
               'Bilbao':{'sul': madrid,
                         'este': barcelona,
                         'oeste': coruna},
               'Barcelona':{'sul': valencia,
                            'oeste': bilbao},
               'Lisboa': {'norte': coruna,
                          'sul': faro,
                          'este': madrid},
               'Madrid': {'norte': bilbao,
                          'sul': sevilla,
                          'este': valencia,
                          'oeste': lisboa},
               'Valencia': {'norte': barcelona,
                            'sul': granada,
                            'oeste': madrid},
               'Faro': {'norte': lisboa,
                        'este': sevilla},
               'Sevilla': {'norte': madrid,
                           'este': granada,
                           'oeste': faro},
               'Granada': {'norte': valencia,
                           'oeste':sevilla}}

    problema_faro_bcn = Problema(faro,[barcelona], viagens)

    acciones_faro = problema_faro_bcn.accoes['Faro']
    nodo_faro = No(faro, None, acciones_faro, None)
    hijos_faro = nodo_faro.expandir(problema_faro_bcn)
    print("filhos de {0}: ".format(nodo_faro.estado.nome))
    print([filho.estado.nome for filho in hijos_faro])


    este_sevilla = problema_faro_bcn.resultado(faro, accE)
    print("{0}".format(este_sevilla.nome))
    acciones_sevilla = problema_faro_bcn.accoes['Sevilla']
    nodo_sevilla = No(este_sevilla, accE, acciones_sevilla, nodo_faro)
    # nodo_faro.hijos.append(nodo_sevilla)
    hijos_sevilla = nodo_sevilla.expandir(problema_faro_bcn)
    print("Hijos de {0}:".format(nodo_sevilla.estado.nome))
    print([hijo.estado.nome for hijo in hijos_sevilla])

    norte_madrid = problema_faro_bcn.resultado(nodo_sevilla.estado, accN)
    print("{0}".format(norte_madrid.nome))
    acciones_madrid = problema_faro_bcn.accoes [ 'Madrid']
    nodo_madrid = No (norte_madrid, accN, acciones_madrid, nodo_sevilla)
    nodo_sevilla.filhos.append(nodo_madrid)
    fin = problema_faro_bcn.e_objectivo (nodo_madrid.estado)
    print("Destino: {0}".format('Sí' if fin else 'No'))
    hijos_madrid = nodo_madrid.expandir(problema_faro_bcn)
    print("Hijos de {0}:".format(nodo_madrid.estado.nome))
    print([hijo.estado.nome for hijo in hijos_madrid])

    este_valencia = problema_faro_bcn.resultado(nodo_madrid.estado, accE)
    print("{0}".format(este_valencia.nome))
    acciones_valencia = problema_faro_bcn.accoes [ 'Valencia']
    nodo_valencia = No(este_valencia, accE, acciones_valencia, nodo_madrid)
    nodo_madrid.filhos.append(nodo_valencia)
    hijos_valencia = nodo_valencia.expandir(problema_faro_bcn)
    print("Hijos de {0}:".format(nodo_valencia.estado.nome))
    print([hijo.estado.nome for hijo in hijos_valencia])

    norte_barcelona = problema_faro_bcn.resultado (nodo_valencia.estado, accN)
    print("{0}".format(norte_barcelona.nome))
    acc_barcelona = problema_faro_bcn.accoes ['Barcelona']
    nodo_barcelona = No (norte_barcelona, accN, acc_barcelona, nodo_valencia)
    nodo_valencia.filhos.append(nodo_barcelona)
    fin = problema_faro_bcn.e_objectivo (nodo_barcelona.estado)
    print("Destino: {0}".format('Si' if fin else 'No'))
'''
'''
coruna = Estado('A Coruña', [accS, accE])
bilbao = Estado('Bilbao', [accS, accE, accO])
barcelona = Estado('Barcelona', [accS, accO])
lisboa = Estado('Lisboa', [accN, accS, accE])
madrid = Estado('Madrid', [accN, accS, accE, accO])
valencia = Estado('Valencia', [accN, accS, accO])
faro = Estado('Faro', [accN, accE])
sevilla = Estado('Sevilla', [accN, accE, accO])
granada = Estado('Granada', [accN, accO])
porto = Estado('Porto', [accN, accS])
giron = Estado('Giron', [accE, accO])

viagens = {'A Coruña': {'sul': porto,
                        'este': giron},
           'Bilbao': {'sul': madrid,
                      'este': barcelona,
                      'oeste': giron},
           'Giron': {'oeste': coruna,
                     'este': bilbao},
           'porto': {'sul': lisboa,
                     'Norte': coruna},
           'Barcelona': {'sul': valencia,
                         'oeste': bilbao},
           'Lisboa': {'norte': porto,
                      'sul': faro,
                      'este': madrid},
           'Madrid': {'norte': bilbao,
                      'sul': sevilla,
                      'este': valencia,
                      'oeste': lisboa},
           'Valencia': {'norte': barcelona,
                        'sul': granada,
                        'oeste': madrid},
           'Faro': {'norte': lisboa,
                    'este': sevilla},
           'Sevilla': {'norte': madrid,
                       'este': granada,
                       'oeste': faro},
           'Granada': {'norte': valencia,
                       'oeste': sevilla}}

kms = {'A Coruña': {'sul': 304,
                    'este': 272},
       'Bilbao': {'sul': 408,
                  'este': 613,
                  'oeste': 272},
       'Giron': {'oeste': 272,
                 'este': 272},
       'porto': {'sul': 304,
                 'Norte': 304},
       'Barcelona': {'sul': 350,
                     'oeste': 613},
       'Lisboa': {'norte': 304,
                  'sul': 278,
                  'este': 624},
       'Madrid': {'norte': 408,
                  'sul': 534,
                  'este': 357,
                  'oeste': 624},
       'Valencia': {'norte': 350,
                    'sul': 487,
                    'oeste': 357},
       'Faro': {'norte': 278,
                'este': 200},
       'Sevilla': {'norte': 534,
                   'este': 252,
                   'oeste': 200},
       'Granada': {'norte': 487,
                   'oeste': 252}}

problema_faro_bcn = Problema(faro, [barcelona], viagens, kms)

accoes_faro = problema_faro_bcn.accoes['Faro']
no_faro = No(faro, None, accoes_faro, None)
filhos_faro = no_faro.expandir(problema_faro_bcn)
print("Filhos de {0}:".format(no_faro.estado.nome))
print([filho.estado.nome for filho in filhos_faro])
menor = no_faro.filho_melhor(problema_faro_bcn)
print("Filho Menor Valor: {0} - {1}".format(menor.estado.nome, problema_faro_bcn.custo_caminho(menor)))

este_sevilla = problema_faro_bcn.resultado(faro, accE)
print("{0}".format(este_sevilla.nome))
acciones_sevilla = problema_faro_bcn.accoes['Sevilla']
nodo_sevilla = No(este_sevilla, accE, acciones_sevilla, no_faro)
no_faro.filhos.append(nodo_sevilla)
dist = problema_faro_bcn.custo_caminho(nodo_sevilla)
print('custo: {0}'.format(dist))
hijos_sevilla = nodo_sevilla.expandir(problema_faro_bcn)
print("Hijos de {0}:".format(nodo_sevilla.estado.nome))
print([hijo.estado.nome for hijo in hijos_sevilla])
menor = nodo_sevilla.filho_melhor(problema_faro_bcn)
print("Filho Menor Valor: {0} - {1}".format(menor.estado.nome, problema_faro_bcn.custo_caminho(menor)))


norte_madrid = problema_faro_bcn.resultado(nodo_sevilla.estado, accN)
print("{0}".format(norte_madrid.nome))
acciones_madrid = problema_faro_bcn.accoes [ 'Madrid']
nodo_madrid = No (norte_madrid, accN, acciones_madrid, nodo_sevilla)
nodo_sevilla.filhos.append(nodo_madrid)
dist = problema_faro_bcn.custo_caminho(nodo_madrid)
print('custo: {0}'.format(dist))
fin = problema_faro_bcn.e_objectivo (nodo_madrid.estado)
print("Destino: {0}".format('Sí' if fin else 'No'))
hijos_madrid = nodo_madrid.expandir(problema_faro_bcn)
print("Hijos de {0}:".format(nodo_madrid.estado.nome))
print([hijo.estado.nome for hijo in hijos_madrid])
menor = nodo_madrid.filho_melhor(problema_faro_bcn)
print("Filho Menor Valor: {0} - {1}".format(menor.estado.nome, problema_faro_bcn.custo_caminho(menor)))


este_valencia = problema_faro_bcn.resultado(nodo_madrid.estado, accE)
print("{0}".format(este_valencia.nome))
acciones_valencia = problema_faro_bcn.accoes [ 'Valencia']
nodo_valencia = No(este_valencia, accE, acciones_valencia, nodo_madrid)
nodo_madrid.filhos.append(nodo_valencia)
dist = problema_faro_bcn.custo_caminho(nodo_valencia)
print('custo: {0}'.format(dist))
hijos_valencia = nodo_valencia.expandir(problema_faro_bcn)
print("Hijos de {0}:".format(nodo_valencia.estado.nome))
print([hijo.estado.nome for hijo in hijos_valencia])
menor = nodo_valencia.filho_melhor(problema_faro_bcn)
print("Filho Menor Valor: {0} - {1}".format(menor.estado.nome, problema_faro_bcn.custo_caminho(menor)))


norte_barcelona = problema_faro_bcn.resultado (nodo_valencia.estado, accN)
print("{0}".format(norte_barcelona.nome))
acc_barcelona = problema_faro_bcn.accoes ['Barcelona']
nodo_barcelona = No (norte_barcelona, accN, acc_barcelona, nodo_valencia)
nodo_valencia.filhos.append(nodo_barcelona)
dist = problema_faro_bcn.custo_caminho(nodo_barcelona)
print('custo: {0}'.format(dist))
fin = problema_faro_bcn.e_objectivo (nodo_barcelona.estado)
print("Destino: {0}".format('Si' if fin else 'No'))
'''
'''
# %% accoes
class Accao:
    def __init__(self, nome):
        self.nome = nome

    def __str__(self):
        return self.nome


# %% Estados
class Estado:
    def __init__(self, nome, accoes):
        self.nome = nome
        self.accoes = accoes

    def __str__(self):
        return self.nome




# %% Problema
class Problema:
    def __init__(self, estado_inicial, estados_objectivos, accoes, custos=None):
        self.estado_inicial = estado_inicial
        self.estados_objectivos = estados_objectivos
        self.accoes = accoes
        self.custos = custos
        self.infinito = 99999

        if not self.custos:
            self.custos = {}
            for estado in self.accoes.keys():
                self.custos[estado] = {}
                for accao in self.accoes[estado].keys():
                    self.custos[estado][accao] = 1

    def __str__(self):
        msg = 'Estado inicial: {0} -> Objectivos: {1}'
        return msg.format(self.estado_inicial.nome,
                          self.estados_objectivos.nome)

    def e_objectivo(self, estado):
        return estado in self.estados_objectivos

    def resultado(self, estado, accao):
        if estado.nome not in self.accoes.keys():
            return None
        accoes_estado = self.accoes[estado.nome]
        if accao.nome not in accoes_estado.keys():
            return None
        return accoes_estado[accao.nome]

    def custo_accao(self, estado, accao):
        if estado.nome not in self.custos.keys():
            return self.infinito
        costes_estado = self.custos[estado.nome]
        if accao.nome not in costes_estado.keys():
            return self.infinito
        return costes_estado[accao.nome]

    def custo_caminho(self, no):
        total = 0
        no = no
        while no.pai:
            total += self.custo_accao(no.pai.estado, no.accao)
            no = no.pai
        return total


# %% No
class No:
    def __init__(self, estado, accao=None, accoes=None, pai=None):
        self.estado = estado
        self.accao = accao
        self.accoes = accoes
        self.pai = pai
        self.filhos = []
        self.custo = 0

    def __str__(self):
        return self.estado.nome

    def expandir(self, problema):
        self.filhos = []
        if not self.accoes :
            if self.estado.nome not in problema.accoes.keys():
                return self.filhos
            self.accoes = problema.accoes[self.estado.nome]
        for accao in self.accoes.keys():
            accao_filho = Accao(accao)
            novo_estado = problema.resultado(self.estado, accao_filho)
            accoes_novo = {}
            if novo_estado.nome in problema.accoes.keys():
                accoes_novo = problema.accoes[novo_estado.nome]
            filho = No(novo_estado, accao_filho, accoes_novo, self)
            custo = self.pai.custo if self.pai else 0
            custo += problema.custo_accao(self.estado, accao_filho)
            filho.custo = custo
            self.filhos.append(filho)
        return self.filhos

    def filho_melhor(self, problema):
        if not self.filhos:
            return None
        melhor = self.filhos[0]
        for filho in self.filhos:
            for objectivo in problema.estados_objectivos:
                custo_caminho_filho = problema.custo_caminho(filho)
                custo_caminho_melhor = problema.custo_caminho(melhor)
                if (custo_caminho_filho < custo_caminho_melhor):
                    melhor = filho
        return melhor
'''