"""
Este é um programa de quiz de futebol que usa a API de futebol para obter dados sobre jogadores de várias ligas de futebol.
O usuário pode escolher a liga e o ano do campeonato, e o programa irá gerar perguntas sobre os jogadores dessa liga e ano.
As categorias do quiz incluem 'artilheiro', 'assistências' e 'cartões amarelos'.
"""

# Importação de bibliotecas necessárias
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
#from tkinter import simpledialog
from PIL import Image, ImageTk
import requests
from io import BytesIO
import random
import json
"""
Pode ser necesserio executar no terminal os comando
pip install Pillow
pip install requests
"""


# Dicionário contendo as ligas de futebol disponíveis para o quiz
ligas = {
    "Premier League": {
        "ID": 39,
        "URL": "https://media.api-sports.io/football/leagues/39.png"
    },
    "Brasileirão": {
        "ID": 71,
        "URL": "https://media.api-sports.io/football/leagues/71.png"
    },
    "Serie A": {
        "ID": 135,
        "URL": "https://media.api-sports.io/football/leagues/135.png"
    },
    "La Liga": {
        "ID": 140,
        "URL": "https://media.api-sports.io/football/leagues/140.png"
    },
    "Ligue 1": {
        "ID": 61,
        "URL": "https://media.api-sports.io/football/leagues/61.png"
    },
    "Bundesliga": {
        "ID": 78,
        "URL": "https://media.api-sports.io/football/leagues/218.png"
    },
    "Champions League": {
        "ID": 2,
        "URL": "https://media.api-sports.io/football/leagues/2.png"
    },
    "Libertadores": {
        "ID": 13,
        "URL": "https://media.api-sports.io/football/leagues/13.png"
    }
}

# Função para fazer uma chamada à API e obter dados sobre os jogadores
def api_futebol():

    if categoria_quiz == 'artilheiro':
        busca_api = 'topscorers'
    elif categoria_quiz == 'assistências':
        busca_api = 'topassists'
    else:
        busca_api = 'topyellowcards'
    url = f"https://api-football-v1.p.rapidapi.com/v3/players/{busca_api}"

    #Teste no console
    #print('url aqui: ', url)

    querystring = {"league": str(liga_escolhida), "season": str(ano_escolhido)}

    #Teste no console
    #print(querystring)

    headers = {
	    "X-RapidAPI-Key": "06f0c1d958mshcd70f7d1495b050p1b4cb5jsnd9f5e358c544",
	    "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code != 200:
        print(f"Erro na requisição: {response.status_code}")
        return
    global data
    data = response.json()
    if 'response' not in data:
        print("Dados esperados não estão presentes na resposta da API")
        return
    #Teste no console
    #print(response.json())


liga_escolhida = None

# Função para solicitar o nome do usuário
def solicitar_nome():
    # Limpar a janela principal
    for widget in window.winfo_children():
        widget.destroy()

    # Solicitar o nome do usuário
    # ctk.CTkLabel(window, text="Por favor, insira seu nome:").grid(row=0, column=0)
    ctk.CTkLabel(window, text="Por favor, insira seu nome:").pack(padx=10, pady=10)
    nome_entry = ctk.CTkEntry(window)
    nome_entry.pack(padx=10, pady=10)
    ctk.CTkButton(window, text="Confirmar", command=lambda: confirmar_nome(nome_entry)).pack(padx=10, pady=10)

# Função para confirmar o nome inserido pelo usuário

def confirmar_nome(entry):
    global nome_usuario
    nome_usuario = entry.get().title()  # Obter o nome do Entry
    if nome_usuario:  # Se um nome foi inserido, mostrar as ligas
        mostrar_carregando("mostrar_ligas()")
    else:
        tk.messagebox.showinfo("Erro", "Por favor, insira seu nome.")

# Função para obter a imagem da liga de futebol
def get_liga_image(url):
    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        print(f"Erro ao fazer a requisição: {e}")

    img_data = response.content
    try:
        img = Image.open(BytesIO(img_data))
    except IOError as e:
        print(f"Erro ao abrir a imagem: {e}")
    img = img.resize((100, 100), Image.Resampling.LANCZOS)  # Redimensionar a imagem
    return ctk.CTkImage(img, size=(100,100))

# Função para exibir as categorias disponíveis para o quiz
def mostrar_categorias():
    # Limpar a janela principal
    
    for widget in window.winfo_children():
        widget.destroy()
    mostrar_carregando("start_quiz(categorias[categoria_atual])")
    #start_quiz(categorias[categoria_atual])

# Função para selecionar a liga de futebol para o quiz
def selecionar_liga(id):
    global liga_escolhida
    liga_escolhida = id
    # Mostrar as categorias do quiz após a seleção da liga
    # mostrar_categorias()
    mostrar_anos()

# Função para exibir as opções de ligas de futebol disponíveis
def mostrar_ligas():
    # Limpar a janela principal

    for widget in window.winfo_children():
        widget.destroy()

    coluna = 0
    fileira = 0
    # Exibir as opções de ligas
    for liga, info in ligas.items():
        photo = get_liga_image(info["URL"])
        btn = ctk.CTkButton(window, image=photo, text=liga, compound="top", command=lambda id=info["ID"]: selecionar_liga(id))
        btn.image = photo  # Manter uma referência da imagem
        btn.grid(row=fileira, column=coluna)  # Posicionar o botão na linha 0 e na coluna atual
        coluna += 1  # Incrementar o contador de colunas para o próximo botão
        if coluna % 2 == 0:
            fileira += 1
            coluna = 0

# Função para exibir as opções de anos disponíveis
def mostrar_anos():
    # Limpar a janela principal
    for widget in window.winfo_children():
        widget.destroy()

    # Label para instrução
    label_instrucao = ctk.CTkLabel(window, text="Escolha o ano do campeonato:")
    label_instrucao.pack()

    # Opções de anos
    anos = list(range(2016, 2024))  # De 2016 a 2023

    # Botões para escolher o ano
    for ano in anos:
        btn_ano = ctk.CTkButton(window, text=str(ano), command=lambda a=ano: selecionar_ano(a))
        btn_ano.pack()

# Função para selecionar o ano para o quiz
def selecionar_ano(ano):
    global ano_escolhido
    ano_escolhido = ano
    messagebox.showinfo("Ano Selecionado", f"Ano {ano_escolhido} foi selecionado.")
    mostrar_categorias()

# Função para baixar e retornar a imagem do jogador a partir da URL
def get_player_image(url):
    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        print(f"Erro ao fazer a requisição: {e}")

    img_data = response.content
    try:
        img = Image.open(BytesIO(img_data))
    except IOError as e:
        print(f"Erro ao abrir a imagem: {e}")
    img = img.resize((100, 100), Image.Resampling.LANCZOS)  # Redimensionar a imagem usando o novo método
    return ctk.CTkImage(img, size=(100,100))

def mostrar_carregando(funcao):
    # Limpar a janela principal
    for widget in window.winfo_children():
        widget.destroy()
    # Exibir mensagem de carregamento
    carregando_label = ctk.CTkLabel(window, text="Carregando...    Aguarde por favor!", font=("arial",30))
    carregando_label.pack(padx=100, pady=100)

    # Atualizar a interface gráfica
    # window.
    window.update_idletasks()

    if "[" in funcao:
    # Aguardar 0,5 segundos antes de continuar
        window.after(500, lambda: eval(funcao))
    
    else:
        window.after(500, eval(funcao))

# Função para gerar o quiz
def generate_quiz(category):
    # Extrair informações dos jogadores
    global all_names
    
    all_players = data['response']
    for player in all_players:
        if 'player' not in player or 'name' not in player['player']:
            print("Dados do jogador estão ausentes ou incompletos")
            return
    
    # Preparar dados para o quiz com base na categoria escolhida
    if category == 'artilheiro':
        all_names = [(player['player']['name'], player['statistics'][0]['goals']['total']) for player in all_players]
    elif category == 'assistências':
        all_names = [(player['player']['name'], player['statistics'][0]['goals']['assists']) for player in all_players]
    else:  # cartões amarelos
        all_names = [(player['player']['name'], player['statistics'][0]['cards']['yellow']) for player in all_players]
    
    #Teste no console
    #print()
    #print('Aqui')
    #print(all_names)
    #print()

    # Ordenar e pegar o nome correto
    all_names.sort(key=lambda x: x[1], reverse=True)
    
    correct_name = all_names[0][0]
    
    # Escolher 4 nomes aleatórios
    global random_names
    random_names = random.sample(all_players, 4)
    random_names = [player['player']['name'] for player in random_names]
    
    # Certificar-se de que o nome correto está na lista
    if correct_name not in random_names:
        random_names.pop()
        random_names.append(correct_name)
    
    # Embaralhar a lista de nomes
    # print(random_names)
    random.shuffle(random_names)
    # print(random_names)
    random.shuffle(random_names)
    print(random_names)
    
    return correct_name, random_names

# Função para fechar a janela do quiz
def close_window():
    window.destroy()

# Função para verificar a resposta
def check_answer(user_choice, correct_answer):
    
    global categoria_atual
    global acertos

    if user_choice == correct_answer:
        acertos += 1
        manipulacao_txt(user_choice, 'correta')
        messagebox.showinfo("Resultado", "Resposta correta!")
    else:
        manipulacao_txt(user_choice, f'errada a resposta correta era {correct_answer}')
        messagebox.showinfo("Resultado", f"Resposta incorreta! A resposta era {correct_answer}!")

    # Incrementar a categoria atual e iniciar o próximo quiz se houver mais categorias
    categoria_atual += 1
    if categoria_atual < len(categorias):
        mostrar_carregando("start_quiz(categorias[categoria_atual])")
        #start_quiz(categorias[categoria_atual])
    else:
        messagebox.showinfo("Fim do Quiz!", "Você completou todas as categorias do quiz!")
        with open('resposta_quiz.txt', 'a') as adicionar:
            adicionar.write(f'{nome_usuario} você acertou: {acertos} de {len(categorias)} quiz\n')
        window.after(500, close_window)  # Aguarda 1 segundos antes de fechar a janela

# Função para obter o nome da Liga com ID
def verificar_liga():
    global chave_correspondente
    for liga, info in ligas.items():
        if info["ID"] == liga_escolhida:
            chave_correspondente = liga
            break
        else:
            chave_correspondente = 'Não encontrada'
            
# Função para manipular o arquivo de texto com as respostas do quiz
def manipulacao_txt(user_choice, resultado):

    with open('resposta_quiz.txt', 'a') as adicionar:
            adicionar.write(f'Nome do usuário: {nome_usuario}\n')
            adicionar.write(f'Liga escolhida: {chave_correspondente}\n')
            adicionar.write(f'Ano escolhido: {ano_escolhido}\n')
            adicionar.write(f'Categoria atual: {categoria_quiz}\n')
            adicionar.write(f'Opções:\n')
            adicionar.write(f'1. {random_names[0]}\n')
            adicionar.write(f'2. {random_names[1]}\n')
            adicionar.write(f'3. {random_names[2]}\n')
            adicionar.write(f'4. {random_names[3]}\n')
            adicionar.write(f'A resposta escolhida foi {user_choice}\n')
            adicionar.write(f'A resposta está {resultado}!\n')


# Função para iniciar o quiz na interface gráfica
def start_quiz(category):
    
    global categoria_quiz
    categoria_quiz = str(category)
    
    #Teste no console
    #print('categoria escolhida', categoria_quiz)

    api_futebol()

    correct_answer, random_names = generate_quiz(category)
    
    # Limpar a interface
    for widget in window.winfo_children():
        widget.destroy()

    # Verificação do nome da liga escolhida pelo usuário
    verificar_liga()

    if category == 'artilheiro':
        texto_quiz = f'Quem é o jogador com mais gol no(a) {chave_correspondente} de {ano_escolhido}?'
    elif category == 'assistências':
        texto_quiz = f'Quem é o jogador com mais assistências no(a) {chave_correspondente} de {ano_escolhido}?'
    else:
        texto_quiz = f'Quem é o jogador com mais cartões amarelos no(a) {chave_correspondente} de {ano_escolhido}?'

    # Exibir a pergunta
    question_label = ctk.CTkLabel(window, text=f"{texto_quiz}")
    question_label.pack()
    print(data['response'])
    random.shuffle(data['response'])
    print(data['response'])
    # Exibir as opções e fotos
    for player in data['response']:
        if player['player']['name'] in random_names:
            # Obter a imagem do jogador
            photo = get_player_image(player['player']['photo'])
            # Criar um botão com a imagem
            btn = ctk.CTkButton(window, image=photo,text="", command=lambda n=player['player']['name']: check_answer(n, correct_answer))
            btn.image = photo  # Manter uma referência da imagem
            btn.pack()
            # Adicionar o nome do jogador abaixo da foto
            name_label = ctk.CTkLabel(window, text=player['player']['name'])
            name_label.pack()

# Configurar a janela principal

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
window = ctk.CTk()
window.geometry("1450x400")
window.title("Chute certeiro!")

try:
    with open('resposta_quiz.txt', 'x'):
        pass
    
except FileExistsError:
    pass

categorias = ['artilheiro', 'assistências', 'cartões amarelos']
random.shuffle(categorias)
categoria_atual = 0
acertos = 0

# Início do quiz solicitando o nome do usuário
solicitar_nome()

# Iniciar o loop da interface gráfica
window.mainloop()


