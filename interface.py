import gettext
import tkinter as tk
from PIL import ImageTk, Image
from tkinter import messagebox
import tkinter.messagebox as tkMessageBox

from grafo import Estado
from grafo import Accao
from grafo import Problema
from grafo import No
from grafo import Caracteristicas
from profundidade_iterativa import *

def show_frame(frame):
    frame.tkraise()


def Calcular():
    msg = 'os dados sao: {0}  {1}  {2}  {3}'.format(cidades_origem.get(), cidades_destino.get()
                                                    , estados_estrada.get(), criterios_escolha.get())
    cidade_origem = cidades_origem.get().lower()
    cidade_destino = cidades_destino.get().lower()
    estado_estrada = int(estados_estrada.get())
    escolha = criterios_escolha.get()
    solucao_busca = chamar_busca(cidade_origem, cidade_destino, estado_estrada, escolha)
    solucao = mostra_solucao(solucao_busca)
    solucao_detalhada = mostra_solucao_detalhada(solucao_busca)
    criterio_total = mostra_criterio_total(escolha, solucao_busca)
    mostrar_solucao_interface(solucao, solucao_detalhada, criterio_total)


def mostrar_solucao_interface(solucao, solucao_detalhada, criterio_total):
    # solucao
    text_area_solucao.delete("1.0", "end")  # Clear existing content
    text_area_solucao.insert("1.0", solucao)

    # Criterio total
    text_area_criterio_total.delete("1.0", "end")  # Clear existing content
    text_area_criterio_total.insert("1.0", criterio_total)

    # detalhes
    # solucao
    text_area_solucao_detalhes.delete("1.0", "end")  # Clear existing content
    text_area_solucao_detalhes.insert("1.0", solucao_detalhada)

    # Criterio total
    text_area_criterio_total_detalhes.delete("1.0", "end")  # Clear existing content
    text_area_criterio_total_detalhes.insert("1.0", criterio_total)



def sair():
    result = tkMessageBox.askquestion("MEDCARE ", "Tem certeza que deseja sair?")
    if result == 'yes':
        janela.destroy()
        exit()


janela = tk.Tk()
janela.iconbitmap('clinic.ico')
janela.rowconfigure(0, weight=1)
janela.columnconfigure(0, weight=1)

frame1 = tk.Frame(janela, bg="#7FBFD3")
frame2 = tk.Frame(janela, bg="#7FBFD3")
frame3 = tk.Frame(janela, bg="#7FBFD3")

for frame in (frame1, frame2, frame3):
    frame.grid(row=0, column=0, sticky="nsew")



# ====== frame 1 code

janela.title(" Sistema de Gestao de pacientes ")
frame1_title = tk.Label(frame1, text=" BEM VINDO AO SISTEMA DE CALCULO DE MELHORES ROTAS EM MOÇAMBIQUE", bg="#7FBFD3",
                        font=" Times 20 bold")
frame1_title.pack()

# imagem
imagem_original = Image.open('Mapa-das-provincias-de-Mocambique.JPG')
largura_desejada = 420
altura_desejada = 565
imagem_redimensionada = imagem_original.resize((largura_desejada, altura_desejada))
imagem = ImageTk.PhotoImage(imagem_redimensionada)
mylabel = tk.Label(frame1, image=imagem)
mylabel.place(x=800, y=80)

# imagem introducao
imagem_original_intro = Image.open('Introducao.png')
largura_desejada = 680
altura_desejada = 565
imagem_redimensionada_intro = imagem_original_intro.resize((largura_desejada, altura_desejada))
imagem_intro = ImageTk.PhotoImage(imagem_redimensionada_intro)
mylabel = tk.Label(frame1, image=imagem_intro)
mylabel.place(x=100, y=80)

lbesp = tk.Label(frame1, text="", bg="#7FBFD3").pack()
# frame1_title = tk.Label(frame1, text=" clicando no botão começar para poder fazer a busca!",
#                         bg="#7FBFD3",
#                         font="Times 18")
# frame1_title.pack()

btn_sair = tk.Button(frame1, text=" Sair ", bg="#D8D6D6", font=" Times 13 bold", bd=2, relief="groove", width=10, command=sair)
btn_sair.place(x=1150, y=700)

frame1_btn = tk.Button(frame1, text="Começar", font=" Times 16 bold", bg="#D9E6EA", width=20, height=1,
                       command=lambda: show_frame(frame2))
frame1_btn.place(x=320, y=699)

# ====== frame 2 code
janela.title(" Sistema de Gestao de pacientes ")
frame1_title = tk.Label(frame2, text="SISTEMA DE CALCULO DE MELHORES ROTAS EM MOÇAMBIQUE", bg="#7FBFD3",
                        font=" Times 20 bold")
frame1_title.pack()
# Label frame Dados da viagem

labelframe_Dados = tk.LabelFrame(frame2, text="Dados da viagem", font=20, bg="#7FBFD3")
labelframe_Dados.pack(anchor="w")

lb_origem = tk.Label(labelframe_Dados, text=" Cidade Origem : ", bg="#7FBFD3", font=" Times 14 bold")
lb_origem.grid(row=0, column=0, sticky="w")

cidades = ['Maputo', 'Matola', 'Xai_xai', 'Inhambane', 'Beira', 'Chimoio', 'Tete', 'Quelimane', 'Nampula',
           'Lichinga', 'Pemba']
cidades_origem = tk.StringVar()
cidades_origem.set(cidades[0])

cidades_origem_drop =  tk.OptionMenu(labelframe_Dados, cidades_origem, *cidades)
cidades_origem_drop.grid(row=0, column=1, sticky="w")

lb_destino = tk.Label(labelframe_Dados, text=" Cidade Destino : ", bg="#7FBFD3", font=" Times 14 bold")
lb_destino.grid(row=0, column=3, sticky="w")

cidades = ['Maputo', 'Matola', 'Xai_xai', 'Inhambane', 'Beira', 'Chimoio', 'Tete', 'Quelimane', 'Nampula',
           'Lichinga', 'Pemba']
cidades_destino = tk.StringVar()
cidades_destino.set(cidades[0])
cidades_destino_drop =  tk.OptionMenu(labelframe_Dados, cidades_destino, *cidades)
cidades_destino_drop.grid(row=0, column=4, sticky="w")

# Criterio e estado da estrada
lb_estrada_estado = tk.Label(labelframe_Dados, text=" estado da estrada: ", bg="#7FBFD3", font=" Times 14 bold")
lb_estrada_estado.grid(row=1, column=0, sticky="w")

estados = ['1', '2', '3', '4', '5']
estados_estrada = tk.StringVar()
estados_estrada.set(estados[0])
estados_estrada_drop =  tk.OptionMenu(labelframe_Dados, estados_estrada, *estados)
estados_estrada_drop.grid(row=1, column=1, sticky="w")

lb_criterio = tk.Label(labelframe_Dados, text=" Criterio: ", bg="#7FBFD3", font=" Times 14 bold")
lb_criterio.grid(row=1, column=3, sticky="w")

criterios = ['distancia', 'duracao', 'custo']
criterios_escolha = tk.StringVar()
criterios_escolha.set(criterios[0])
criterios_escolha_drop =  tk.OptionMenu(labelframe_Dados, criterios_escolha, *criterios)
criterios_escolha_drop.grid(row=1, column=4, sticky="w")

#botao calcular
calcular_btn = tk.Button(labelframe_Dados, text="Calcular", font=" Times 16 bold", bg="#D9E6EA", width=10, height=1,
                       command=lambda: Calcular())
calcular_btn.grid(row=2, column=2, sticky="w")


# Mostrar Solucao
# Label frame Dados da viagem

labelframe_solucao = tk.LabelFrame(frame2, text="Mostrar Solução", font=20, bg="#7FBFD3")
labelframe_solucao.pack(anchor="w")

lb_solucao = tk.Label(labelframe_solucao, text=" Solução : ", bg="#7FBFD3", font=" Times 14 bold")
lb_solucao.pack(anchor="w")

text_area_solucao = tk.Text(labelframe_solucao, height=11, width=60, font=" Times 18")
text_area_solucao.pack(pady=10)

# criterio total
lb_criterio_total = tk.Label(labelframe_solucao, text=" Criterio total: ", bg="#7FBFD3", font=" Times 14 bold")
lb_criterio_total.pack(anchor="w")

text_area_criterio_total = tk.Text(labelframe_solucao, height=2, width=60, font=" Times 18")
text_area_criterio_total.pack(pady=10)

#botao detalhes
detalhes_btn = tk.Button(labelframe_solucao, text="Mais Detalhes", font=" Times 16 bold", bg="#D9E6EA", width=15, height=1,
                       command=lambda: show_frame(frame3))
detalhes_btn.pack(pady=10)

# imagem
mylabel = tk.Label(frame2, image=imagem)
mylabel.place(x=800, y=80)



btn_voltar = tk.Button(frame2, text=" Voltar", bg="#D3D3D3", font=" Times 13 bold", bd=2, relief="groove", width=10,
                  command=lambda: show_frame(frame1))
btn_voltar.place(x=1000, y=700)

btn_sair = tk.Button(frame2, text=" Sair ", bg="#D8D6D6", font=" Times 13 bold", bd=2, relief="groove", width=10, command=sair)
btn_sair.place(x=1150, y=700)


# ====== frame 3 code
frame3_title = tk.Label(frame3, text="Detalhes da Rota ", font='Italic  22 ', bg="#7FBFD3")
frame3_title.pack()

# imagem
mylabel = tk.Label(frame3, image=imagem)
mylabel.place(x=800, y=80)

lb_solucao = tk.Label(frame3, text=" Solução : ", bg="#7FBFD3", font=" Times 14 bold")
lb_solucao.pack(anchor="w")

text_area_solucao_detalhes = tk.Text(frame3, height=20, width=60, font=" Times 18")
text_area_solucao_detalhes.pack(anchor="w")

# criterio total
lb_criterio_total = tk.Label(frame3, text=" Criterio total: ", bg="#7FBFD3", font=" Times 14 bold")
lb_criterio_total.pack(anchor="w")

text_area_criterio_total_detalhes = tk.Text(frame3, height=2, width=60, font=" Times 18")
text_area_criterio_total_detalhes.pack(anchor="w")

btn_voltar = tk.Button(frame3, text=" Voltar", bg="#D3D3D3", font=" Times 13 bold", bd=2, relief="groove", width=10,
                  command=lambda: show_frame(frame2))
btn_voltar.place(x=1000, y=700)

btn_sair = tk.Button(frame3, text=" Sair ", bg="#D8D6D6", font=" Times 13 bold", bd=2, relief="groove", width=10, command=sair)
btn_sair.place(x=1150, y=700)


show_frame(frame1)

janela.resizable(False, False)
janela.geometry("1280x760+100+20")
janela.mainloop()



