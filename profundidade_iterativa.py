from grafo import Estado
from grafo import Accao
from grafo import Problema
from grafo import No
from grafo import Caracteristicas
# Profundidade

def profundidade_iterativa_com_custo(problema):
    for i in range(1, 1111111, 1):
        raiz = cria_no_raiz (problema)
        explorados = set()
        solucoes = []
        __custo_recursiva(raiz, problema, explorados, solucoes)
        if solucoes:
            for solucao in solucoes:
                mostra_solucao(solucao)
                # print('', end='\n')
            if problema.escolha == 'distancia':
                melhor = min(solucoes, key=lambda no: no.distancia)
            elif problema.escolha == 'duracao':
                melhor = min(solucoes, key=lambda no: no.duracao)
            else:
                melhor = min(solucoes, key=lambda no: no.custo)
            return melhor
    return None

def __custo_recursiva(nodo, problema, explorados, solucoes):
    if problema.e_objectivo(nodo.estado):
        solucoes.append(nodo)
        return nodo
    explorados.add(nodo.estado)
    if not nodo.accoes:
        return None
    for nombre_accion in nodo.accoes.keys():
        #accion = Accao (nombre_accion)
        accion = globals()[nombre_accion]
        hijo = cria_no_filho (problema, nodo, accion)
        if hijo.estado not in explorados and accion.caracteristicas.piso >= problema.piso_min:
            distancia = problema.distancia_accao(nodo.estado, accion)
            __custo_recursiva (hijo, problema, explorados.copy(), solucoes)

    return None


# metodos
def cria_no_raiz(problema):
    estado_raiz = problema.estado_inicial
    accoes_raiz = {}
    if estado_raiz.nome in problema.accoes.keys():
        accoes_raiz = problema.accoes[estado_raiz.nome]
    raiz = No(estado_raiz, None, accoes_raiz, None)
    raiz.custo = 0
    raiz.distancia = 0
    raiz.duracao = 0
    return raiz


def cria_no_filho(problema, pai, accao):
    nuevo_estado = problema.resultado(pai.estado, accao)
    acciones_nuevo = {}
    if nuevo_estado.nome in problema.accoes.keys():
        acciones_nuevo = problema.accoes[nuevo_estado.nome]
    filho = No(nuevo_estado, accao, acciones_nuevo, pai)

    custo = pai.custo
    custo += problema.custo_accao(pai.estado, accao)
    filho.custo = custo

    distancia = pai.distancia
    distancia += problema.distancia_accao(pai.estado, accao)
    filho.distancia = distancia

    duracao = pai.duracao
    duracao += problema.duracao_accao(pai.estado, accao)
    filho.duracao = duracao

    pai.filhos.append(filho)
    return filho


def mostra_solucao_detalhada(objetivo=None):
    if not objetivo:
            print("Não Há solucão")
            return
    no = objetivo
    solucao_final = []
    while no:
        msg = "{0} [dist:{1}km, dur:{2:.1f}h, custo:{3:.2f}mzn]"
        estado = no.estado.nome
        custo_total = no.custo
        distancia_total = no.distancia
        duracao_total = no.duracao
        # print(msg.format(estado.upper(), distancia_total, duracao_total, custo_total), end=" ")
        msg = msg.format(estado.upper(), distancia_total, duracao_total, custo_total) + ' '
        solucao_final.append(msg)
        if no.accao:
            msg_accao = " --({0}  [dist:{1}km, dur:{2:.1f}h, custo:{3:.2f}mzn])--> "
            duracao = duracao_calc(no.accao)
            custo = calcular_custo_medio(no.accao)
            # print(msg_accao.format(no.accao.nome, no.accao.distancia, duracao, custo), end=" ")
            msg_accao = msg_accao.format(no.accao.nome, no.accao.distancia, duracao, custo)
            solucao_final.append(msg_accao)
        no = no.pai
    solucao = ''
    for elemento in reversed(solucao_final):
        # print(elemento, end=" ")
        solucao += elemento + "\n\n"
    return solucao

def mostra_solucao(objetivo=None):
    if not objetivo:
            print("Não Há solucão")
            return "Não Há solucão"
    no = objetivo
    solucao_final = []
    while no:
        msg = "{0}"
        estado = no.estado.nome
        # print(msg.format(estado.upper(), distancia_total, duracao_total, custo_total), end=" ")
        msg = msg.format(estado.upper()) + ' '
        solucao_final.append(msg)
        if no.accao:
            msg_accao = " --({0})-> "
            # print(msg_accao.format(no.accao.nome, no.accao.distancia, duracao, custo), end=" ")
            msg_accao = msg_accao.format(no.accao.nome)  + "\n"
            solucao_final.append(msg_accao)
        no = no.pai
    solucao = ''
    for elemento in reversed(solucao_final):
        # print(elemento, end=" ")
        solucao += elemento
    return solucao

def mostra_criterio_total(escolha, objetivo=None):
    if not objetivo:
            print("Não Há solucão")
            return "Não Há solucão"
    no = objetivo
    msg = ''
    if escolha == 'distancia':
        msg = 'O total da distância é: {}km'.format(round(no.distancia, 2))
    elif escolha == 'duracao':
        msg = 'O total da duração é: {}h'.format(round(no.duracao, 2))
    else:
        msg = 'O total é do custo é: {}mzn'.format(round(no.custo, 2))
    return msg

def chamar_busca(origem, destino, piso_minimo, escolha):
    origem = globals()[origem]
    destino = globals()[destino]
    problema_resolver = Problema(origem, [destino], viagens, piso_minimo, distancias, duracao, custo_medio
                                 , escolha)
    solucao = profundidade_iterativa_com_custo(problema_resolver)
    print(mostra_solucao(solucao))
    print(mostra_criterio_total(escolha, solucao))
    # mostrar_solucao_interface(mostra_solucao(solucao), mostra_criterio_total(escolha, solucao))
    return solucao


def calcular_custo_medio(n):
    distancia = n.distancia
    portagem = n.caracteristicas.portagem
    if distancia == 0:
        return portagem
    else:
        gasto_combustivel = (distancia / 14) * 86.25
        return gasto_combustivel + portagem

def duracao_calc(n):
    return n.distancia / n.caracteristicas.velocidade_media


# %% Definicoes

'''
n1 = Accao('n1', 'beira','Inhambane',278, Caracteristicas(5,500,130))
n2 = Accao('n2', 'beira','quelimane',304, Caracteristicas(5,500,130))
n3 = Accao('n3', 'beira','quelimane',304, Caracteristicas(5,500,90))
n4 = Accao('n4', 'beira','quelimane',272, Caracteristicas(5,0,70))
n5 = Accao('n5', 'beira','tete',272, Caracteristicas(5,500,130))
n6 = Accao('n6', 'beira','xai-xai',613, Caracteristicas(2,0,60))
n7 = Accao('n7', 'quelimane', 'nampula',624, Caracteristicas(4,0,100))
n8 = Accao('n8', 'tete','maputo',200, Caracteristicas(3,0,80))
n9 = Accao('n9', 'tete','dondo',252, Caracteristicas(2,0,60))
n10 = Accao('n10', 'tete','songo',534, Caracteristicas(3,0,80))
n11 = Accao('n11', 'xai-xai','tete',487, Caracteristicas(1,0,50))
n12 = Accao('n12', 'xai-xai', 'songo',357, Caracteristicas(3,0,90))
n13 = Accao('n13', 'nampula', 'vilanculos',408, Caracteristicas(2,0,70))
n14 = Accao('n14', 'vilanculos','Inhambane',350, Caracteristicas(3,0,60))


coruna = Estado('A Coruña', [n3, n4])
bilbao = Estado('Bilbao', [n5, n6, n13])
barcelona = Estado('Barcelona', [n6, n14])
lisboa = Estado('Lisboa', [n1, n2, n7])
madrid = Estado('Madrid', [n7, n10, n13, n12])
valencia = Estado('Valencia', [n11, n12, n14])
faro = Estado('Faro', [n1, n8])
sevilla = Estado('Sevilla', [n8, n9, n10])
granada = Estado('Granada',[n9,n11])
porto = Estado('Porto', [n2, n3])
giron = Estado('Giron',[n4,n5])



viagens = {'A Coruña': {'n3': porto,
                        'n4': giron},
           'Bilbao': {'n13': madrid,
                      'n6': barcelona,
                      'n5': giron},
           'Giron': {'n4': coruna,
                     'n5': bilbao},
           'porto': {'n2': lisboa,
                     'n3': coruna},
           'Barcelona': {'n14': valencia,
                         'n6': bilbao},
           'Lisboa': {'n2': porto,
                      'n1': faro,
                      'n7': madrid},
           'Madrid': {'n13': bilbao,
                      'n10': sevilla,
                      'n12': valencia,
                      'n7': lisboa},
           'Valencia': {'n14': barcelona,
                        'n11': granada,
                        'n12': madrid},
           'Faro': {'n1': lisboa,
                    'n8': sevilla},
           'Sevilla': {'n10': madrid,
                       'n9': granada,
                       'n8': faro},
           'Granada': {'n11': valencia,
                       'n9': sevilla}}



distancias = {'A Coruña': {'n3': 304,
                    'n4': 272},
       'Bilbao': {'n13': 408,
                  'n6': 613,
                  'n5': 272},
       'Giron': {'n4': 272,
                 'n5': 272},
       'porto': {'n2': 304,
                 'n3': 304},
       'Barcelona': {'n14': 350,
                     'n6': 613},
              'Lisboa': {'n2': 304,
                  'n1': 278,
                  'n7': 624},
              'Madrid': {'n13': 408,
                  'n10': 534,
                  'n12': 357,
                  'n7': 624},
              'Valencia': {'n14': 350,
                    'n11': 487,
                    'n12': 357},
              'Faro': {'n1': 278,
                'n8': 200},
              'Sevilla': {'n10': 534,
                   'n9': 252,
                   'n8': 200},
              'Granada': {'n11': 487,
                   'n9': 252}}



duracao = {'A Coruña': {'n3': duracao_calc(n3),
                    'n4': duracao_calc(n4)},
       'Bilbao': {'n13': duracao_calc(n13),
                  'n6': duracao_calc(n6),
                  'n5': duracao_calc(n5)},
       'Giron': {'n4': duracao_calc(n4),
                 'n5': duracao_calc(n5)},
       'porto': {'n2': duracao_calc(n2),
                 'n3': duracao_calc(n3)},
       'Barcelona': {'n14': duracao_calc(n14),
                     'n6': duracao_calc(n6)},
       'Lisboa': {'n2': duracao_calc(n2),
                  'n1': duracao_calc(n1),
                  'n7': duracao_calc(n7)},
       'Madrid': {'n13': duracao_calc(n13),
                  'n10': duracao_calc(n10),
                  'n12': duracao_calc(n12),
                  'n7': duracao_calc(n7)},
       'Valencia': {'n14': duracao_calc(n14),
                    'n11': duracao_calc(n11),
                    'n12': duracao_calc(n12)},
       'Faro': {'n1': duracao_calc(n1),
                'n8': duracao_calc(n8)},
       'Sevilla': {'n10': duracao_calc(n10),
                   'n9': duracao_calc(n9),
                   'n8': duracao_calc(n8)},
       'Granada': {'n11': duracao_calc(n11),
                   'n9': duracao_calc(n9)}}




custo_medio = {'A Coruña': {'n3': calcular_gasto_medio(n3),
                    'n4': calcular_gasto_medio(n4)},
       'Bilbao': {'n13': calcular_gasto_medio(n13),
                  'n6': calcular_gasto_medio(n6),
                  'n5': calcular_gasto_medio(n5)},
       'Giron': {'n4': calcular_gasto_medio(n4),
                 'n5': calcular_gasto_medio(n5)},
       'porto': {'n2': calcular_gasto_medio(n2),
                 'n3': calcular_gasto_medio(n3)},
       'Barcelona': {'n14': calcular_gasto_medio(n14),
                     'n6': calcular_gasto_medio(n6)},
       'Lisboa': {'n2': calcular_gasto_medio(n2),
                  'n1': calcular_gasto_medio(n1),
                  'n7': calcular_gasto_medio(n7)},
       'Madrid': {'n13': calcular_gasto_medio(n13),
                  'n10': calcular_gasto_medio(n10),
                  'n12': calcular_gasto_medio(n12),
                  'n7': calcular_gasto_medio(n7)},
       'Valencia': {'n14': calcular_gasto_medio(n14),
                    'n11': calcular_gasto_medio(n11),
                    'n12': calcular_gasto_medio(n12)},
       'Faro': {'n1': calcular_gasto_medio(n1),
                'n8': calcular_gasto_medio(n8)},
       'Sevilla': {'n10': calcular_gasto_medio(n10),
                   'n9': calcular_gasto_medio(n9),
                   'n8': calcular_gasto_medio(n8)},
       'Granada': {'n11': calcular_gasto_medio(n11),
                   'n9': calcular_gasto_medio(n9)}}
'''

en1 = Accao('en1', 'Maputo','Xai-xai',214, Caracteristicas(4,160,100))
en4 = Accao('en4', 'Maputo','Matola',23, Caracteristicas(3,40,60))
en1_1 = Accao('en1_1', 'Matola','Xai-xai',229, Caracteristicas(4,160,80))
en1_3 = Accao('en1_3', 'Xai-xai','Chimoio',948, Caracteristicas(3,160,120))
en1_2 = Accao('en1_2', 'Xai-xai','Inhambane',260.6, Caracteristicas(2,420,120))
en1_4 = Accao('en1_4', 'Inhambane','Chimoio',744, Caracteristicas(1,160,80))
en1_5 = Accao('en1_5', 'Inhambane', 'Beira',719, Caracteristicas(2,40,100))
en6 = Accao('en6', 'Chimoio','Beira',212, Caracteristicas(3,0,120))
en7 = Accao('en7', 'Chimoio','Tete',388, Caracteristicas(2,0,60))
en6_3 = Accao('en6_3', 'Beira','Tete',589, Caracteristicas(3,0,80))
en6_1 = Accao('en6_1', 'Beira','Quelimane',484, Caracteristicas(1,40,60))
en6_2 = Accao('en6_2', 'Quelimane', 'Tete',699, Caracteristicas(3,160,90))
en8_1 = Accao('en8_1', 'Quelimane', 'Lichinga',805, Caracteristicas(2,0,70))
en8 = Accao('en8', 'Quelimane','Nampula',546, Caracteristicas(3,160,60))
en14 = Accao('en14', 'Nampula','Lichinga',689, Caracteristicas(3,40,80))
en8_2 = Accao('en8_2', 'Nampula','Pemba',407, Caracteristicas(3,160,100))
en14_1 = Accao('en14_1', 'Lichinga','Pemba',727, Caracteristicas(4,160,100))


matola = Estado('Matola', [en1_1, en4])
maputo = Estado('Maputo', [en4, en1])
xai_xai = Estado('Xai-xai', [en1_1, en1, en1_2, en1_3])
inhambane = Estado('Inhambane', [en1_2, en1_4, en1_5])
beira = Estado('Beira', [en1_5, en6, en6_3, en6_1])
chimoio = Estado('Chimoio', [en1_3, en1_4, en6, en7])
tete = Estado('Tete', [en7, en6_3, en6_2])
quelimane = Estado('Quelimane', [en6_1, en6_2, en8_1, en8])
nampula = Estado('Nampula',[en8, en14, en8_2])
lichinga = Estado('Lichinga', [en8_1, en14, en14_1])
pemba = Estado('Pemba',[en8_2,en14_1])



viagens = {'Matola': {'en1_1': xai_xai,
                        'en4': maputo},
           'Maputo': {'en4': matola,
                      'en1': xai_xai},
           'Xai-xai': {'en1_1': matola,
                     'en1': maputo,
                      'en1_2': inhambane,
                      'en1_3': chimoio,},
           'Inhambane': {'en1_2': xai_xai,
                     'en1_4': chimoio,
                     'en1_5': beira},
           'Beira': {'en1_5': inhambane,
                         'en6': chimoio,
                          'en6_3': tete,
                          'en6_1': quelimane},
           'Chimoio': {'en1_3': xai_xai,
                      'en1_4': inhambane,
                      'en6': beira,
                       'en7': tete},
           'Tete': {'en7': chimoio,
                      'en6_3': beira,
                      'en6_2': quelimane},
           'Quelimane': {'en6_1': beira,
                        'en6_2': tete,
                        'en8_1': lichinga,
                         'en8': nampula},
           'Nampula': {'en8': quelimane,
                    'en14': lichinga,
                     'en8_2': pemba},
           'Lichinga': {'en8_1': quelimane,
                       'en14': nampula,
                       'en14_1': pemba},
           'Pemba': {'en8_2': nampula,
                       'en14_1': lichinga}}



distancias = {'Matola': {'en1_1': en1_1.distancia,
                        'en4': en4.distancia},
           'Maputo': {'en4': en4.distancia,
                      'en1': en1.distancia},
           'Xai-xai': {'en1_1': en1_1.distancia,
                     'en1': en1.distancia,
                      'en1_2': en1_2.distancia,
                      'en1_3': en1_3.distancia,},
           'Inhambane': {'en1_2': en1_2.distancia,
                     'en1_4': en1_4.distancia,
                     'en1_5': en1_5.distancia},
           'Beira': {'en1_5': en1_5.distancia,
                         'en6': en6.distancia,
                          'en6_3': en6_3.distancia,
                          'en6_1': en6_1.distancia},
           'Chimoio': {'en1_3': en1_3.distancia,
                      'en1_4': en1_4.distancia,
                      'en6': en6.distancia,
                       'en7': en7.distancia},
           'Tete': {'en7': en7.distancia,
                      'en6_3': en6_3.distancia,
                      'en6_2': en6_2.distancia},
           'Quelimane': {'en6_1': en6_1.distancia,
                        'en6_2': en6_2.distancia,
                        'en8_1': en8_1.distancia,
                         'en8': en8.distancia},
           'Nampula': {'en8': en8.distancia,
                    'en14': en14.distancia,
                     'en8_2': en8_2.distancia},
           'Lichinga': {'en8_1': en8_1.distancia,
                       'en14': en14.distancia,
                       'en14_1': en14_1.distancia},
           'Pemba': {'en8_2': en8_2.distancia,
                       'en14_1': en14_1.distancia}}

#*****************************************************************************************
duracao = {'Matola': {'en1_1': duracao_calc(en1_1),
                        'en4': duracao_calc(en4)},
           'Maputo': {'en4': duracao_calc(en4)},
                      'en1': duracao_calc(en1),
           'Xai-xai': {'en1_1': duracao_calc(en1_1),
                     'en1': duracao_calc(en1),
                      'en1_2': duracao_calc(en1_2),
                      'en1_3': duracao_calc(en1_3)},
           'Inhambane': {'en1_2': duracao_calc(en1_2),
                     'en1_4': duracao_calc(en1_4),
                     'en1_5': duracao_calc(en1_5)},
           'Beira': {'en1_5': duracao_calc(en1_5),
                         'en6': duracao_calc(en6),
                          'en6_3': duracao_calc(en6_3),
                          'en6_1': duracao_calc(en6_1)},
           'Chimoio': {'en1_3': duracao_calc(en1_3),
                      'en1_4': duracao_calc(en1_4),
                      'en6': duracao_calc(en6),
                       'en7': duracao_calc(en7)},
           'Tete': {'en7': duracao_calc(en7),
                      'en6_3': duracao_calc(en6_3),
                      'en6_2': duracao_calc(en6_2)},
           'Quelimane': {'en6_1': duracao_calc(en6_1),
                        'en6_2': duracao_calc(en6_2),
                        'en8_1': duracao_calc(en8_1),
                         'en8': duracao_calc(en8)},
           'Nampula': {'en8': duracao_calc(en8),
                    'en14': duracao_calc(en14),
                     'en8_2': duracao_calc(en8_2)},
           'Lichinga': {'en8_1': duracao_calc(en8_1),
                       'en14': duracao_calc(en14),
                       'en14_1': duracao_calc(en14_1)},
           'Pemba': {'en8_2': duracao_calc(en8_2),
                       'en14_1': duracao_calc(en14_1)}}



custo_medio = {'Matola': {'en1_1': calcular_custo_medio(en1_1),
                        'en4': calcular_custo_medio(en4)},
           'Maputo': {'en4': calcular_custo_medio(en4),
                      'en1': calcular_custo_medio(en1),
           'Xai-xai': {'en1_1': calcular_custo_medio(en1_1),
                     'en1': calcular_custo_medio(en1),
                      'en1_2': calcular_custo_medio(en1_2),
                      'en1_3': calcular_custo_medio(en1_3)},
           'Inhambane': {'en1_2': calcular_custo_medio(en1_2),
                     'en1_4': calcular_custo_medio(en1_4),
                     'en1_5': calcular_custo_medio(en1_5)},
           'Beira': {'en1_5': calcular_custo_medio(en1_5),
                         'en6': calcular_custo_medio(en6),
                          'en6_3': calcular_custo_medio(en6_3),
                          'en6_1': calcular_custo_medio(en6_1)},
           'Chimoio': {'en1_3': calcular_custo_medio(en1_3),
                      'en1_4': calcular_custo_medio(en1_4),
                      'en6': calcular_custo_medio(en6),
                       'en7': calcular_custo_medio(en7)},
           'Tete': {'en7': calcular_custo_medio(en7),
                      'en6_3': calcular_custo_medio(en6_3),
                      'en6_2': calcular_custo_medio(en6_2)},
           'Quelimane': {'en6_1': calcular_custo_medio(en6_1),
                        'en6_2': calcular_custo_medio(en6_2),
                        'en8_1': calcular_custo_medio(en8_1),
                         'en8': calcular_custo_medio(en8)},
           'Nampula': {'en8': calcular_custo_medio(en8),
                    'en14': calcular_custo_medio(en14),
                     'en8_2': calcular_custo_medio(en8_2)},
           'Lichinga': {'en8_1': calcular_custo_medio(en8_1),
                       'en14': calcular_custo_medio(en14),
                       'en14_1': calcular_custo_medio(en14_1)},
           'Pemba': {'en8_2': calcular_custo_medio(en8_2),
                       'en14_1': calcular_custo_medio(en14_1)}}}
# piso_minimo = 2
# escolha = 'custo'
# problema_resolver = Problema(faro, [barcelona], viagens, piso_minimo, distancias, duracao, custo_medio
#                                  , escolha)
# solucao = profundidade_iterativa_com_custo(problema_resolver)
# mostra_solucao(solucao)
# print(mostra_criterio_total(escolha, solucao))




'''
# Vias
a4 = dados_via('a4', 'beira','Inhambane',65, caracteristicas(5,500,130))
a1 = dados_via('a1', 'beira','quelimane',70, caracteristicas(5,500,130))
n1 = dados_via('n1', 'beira','quelimane',70, caracteristicas(5,500,90))
n109 = dados_via('n109', 'beira','quelimane',60, caracteristicas(5,0,70))
n10 = dados_via('n10', 'beira','tete',50, caracteristicas(5,500,130))
ip1 = dados_via('ip1', 'beira','xai-xai',30, caracteristicas(2,0,60))
n6 = dados_via('n6', 'quelimane', 'nampula',70, caracteristicas(4,0,100))
n23 = dados_via('n23', 'tete','maputo',130, caracteristicas(3,0,80))
n35 = dados_via('n35', 'tete','dondo',25, caracteristicas(2,0,60))
ic1 = dados_via('ic1', 'tete','songo',55, caracteristicas(3,0,80))
n31 = dados_via('n31', 'xai-xai','tete',25, caracteristicas(1,0,50))
ip11 = dados_via('ip1', 'xai-xai', 'songo',45, caracteristicas(3,0,90))
n61 = dados_via('n6', 'nampula', 'vilanculos',70, caracteristicas(2,0,70))
n18 = dados_via('n18', 'vilanculos','Inhambane',50, caracteristicas(2,0,60))
n19 = dados_via('n19', 'vilanculos','vilareal', 40, caracteristicas(2,0,60))
n351 = dados_via('n35', 'dondo', 'Inhambane', 40, caracteristicas(2,0,60))
a41 = dados_via('a4', 'Inharrime', 'Inhambane', 40, caracteristicas(1,400,120))
ip2 = dados_via('ip2', 'Inharrime', 'maputo', 65, caracteristicas(2,0,60))

beira = Estado('Beira', [a4, a1, n1, n109, n10, ip1])
quelimane = Estado('Quelimane', [a1, n1, n109, n6])
tete = Estado('Tete', [n10, n23, n35, ic1, n351, n31])
xai_xai = Estado('Xai-xai', [ip11, n31, ic1, ip11])
nampula = Estado('Nampula', [n6, n61])
vilanculos = Estado('Vilanculos', [n61, n18, n19])
dondo = Estado('Dondo', [n35, n351])
inharrime = Estado('Inharrime', [a4, ip2])
songo = Estado('Songo',[ic1, ip11])
vilareal = Estado('vilareal', [n19])
maputo = Estado('Maputo',[n23, ip2])
Inhambane = Estado('Maputo',[a4, n18, n351, a41])
'''

'''
from grafo import Estado
from grafo import Accao
from grafo import Problema
from grafo import No

# Profundidade

def profundidade_iterativa_com_custo(problema, limite=99999, passo=1):
    for i in range(1, limite + 1, passo):
        raiz = cria_no_raiz (problema)
        explorados = set()
        solucoes = []
        __custo_recursiva(raiz, problema, limite, explorados, solucoes)
        if solucoes:
            melhor = min(solucoes, key=lambda no: no.custo)
            return melhor
    return None

def __custo_recursiva(nodo, problema, limite, explorados, solucoes):
    if limite <= 0:
        return None
    if problema.e_objectivo(nodo.estado):
        solucoes.append(nodo)
        return nodo
    explorados.add(nodo.estado)
    if not nodo.accoes:
        return None
    for nombre_accion in nodo.accoes.keys():
        accion = Accao (nombre_accion)
        hijo = cria_no_filho (problema, nodo, accion)
        if hijo.estado not in explorados:
            custo = problema.custo_accao(nodo.estado, accion)
            __custo_recursiva (hijo, problema, limite - custo, explorados.copy(), solucoes)
    return None


# metodos
def cria_no_raiz(problema):
    estado_raiz = problema.estado_inicial
    accoes_raiz = {}
    if estado_raiz.nome in problema.accoes.keys():
        accoes_raiz = problema.accoes[estado_raiz.nome]
    raiz = No(estado_raiz, None, accoes_raiz, None)
    raiz.custo = 0
    return raiz


def cria_no_filho(problema, pai, accao):
    nuevo_estado = problema.resultado(pai.estado, accao)
    acciones_nuevo = {}
    if nuevo_estado.nome in problema.accoes.keys():
        acciones_nuevo = problema.accoes[nuevo_estado.nome]
    filho = No(nuevo_estado, accao, acciones_nuevo, pai)
    custo = pai.custo
    custo += problema.custo_accao(pai.estado, accao)
    filho.custo = custo
    pai.filhos.append(filho)
    return filho


def mostra_solucao(objetivo=None):
    if not objetivo:
            print("Não Há solucão")
            return
    no = objetivo
    while no:
        msg = "{0}[{1}]"
        estado = no.estado.nome
        custo_total = no.custo
        print(msg.format(estado, custo_total), end=" ")
        if no.accao:
            msg = "<--({0})--"
            print(msg.format(no.accao.nome), end=" ")
        no = no.pai


# %% Definicoes
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
porto = Estado('Porto', [accN, accS])
giron = Estado('Giron',[accE,accO])

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

custos = {'A Coruña': {'sul': 304,
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


problema_resolver = Problema(faro, [barcelona], viagens, custos)
solucao = profundidade_iterativa_com_custo(problema_resolver)
mostra_solucao(solucao)
'''