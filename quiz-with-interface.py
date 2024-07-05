"""
Este é um programa de quiz de futebol que usa a API-FOOTBALL (https://rapidapi.com/api-sports/api/api-football/details). 
Para obter dados sobre jogadores de várias ligas de futebol.
O usuário pode escolher a liga e o ano do campeonato, e o programa irá gerar perguntas sobre os jogadores dessa liga e ano.
As categorias do quiz incluem 'artilheiro', 'assistências' e 'cartões amarelos'.
"""
# Importando as bibliotecas necessárias
import flet as ft # https://flet.dev/docs/
import requests # https://pypi.org/project/requests/
import random # https://docs.python.org/pt-br/3/library/random.html
import json # https://docs.python.org/3/library/json.html
import time # https://docs.python.org/3/library/time.html
import os # https://docs.python.org/3/library/os.html
import datetime # https://docs.python.org/3/library/datetime.html
"""
Pode ser necesserio executar no terminal os comando
pip install Flet
pip install requests
"""

# Dicionário contendo as ligas de futebol disponíveis para o quiz
ligas = {
    "Premier": {"ID": 39, "URL": "https://media.api-sports.io/football/leagues/39.png"},
    "Brasileirão": {"ID": 71, "URL": "https://media.api-sports.io/football/leagues/71.png"},
    "Serie A": {"ID": 135, "URL": "https://media.api-sports.io/football/leagues/135.png"},
    "La Liga": {"ID": 140, "URL": "https://media.api-sports.io/football/leagues/140.png"},
    "Ligue 1": {"ID": 61, "URL": "https://media.api-sports.io/football/leagues/61.png"},
    "Bundesliga": {"ID": 78, "URL": "https://media.api-sports.io/football/leagues/218.png"},
    "Champions": {"ID": 2, "URL": "https://media.api-sports.io/football/leagues/2.png"},
    "Libertadores": {"ID": 13, "URL": "https://media.api-sports.io/football/leagues/13.png"}
}

CONFIG = {
    "COLOR_TEXT": "black",
    "COLOR_TEXT_IN_BUTTON": "white",
    "COLOR_TEXT_IN_CONTAINER": "white",
    "SIZE_BUTTON": 250,
    "SIZE_BUTTON_CONFIRM": 130
}

nome_usuario = ""
liga_selecionada = ""
ano_selecionado = ""
acertos = 0
data = {}
random_names = []
correct_answer = ""
categoria_quiz = ""
chave_correspondente = ""
url_liga = ""
nome_usuario = ""
liga_selecionada = ""
ano_selecionado = ""
caminho_arquivo = ''
categoria_atual = 0

categorias = ['artilheiro', 'assistências', 'cartões']
nome_arquivo_keys = 'keys_api.json'
max_interacoes = 100

def main(page: ft.Page):
    reset_vars()
    
    categoria_atual = 0
    random.shuffle(categorias)
    configurar_pagina(page)
    verificar_arquivo_interacoes()
    if interacoes_restantes():
        solicitar_nome(page)
    else:
        texto_tela(page, True, "Limite de interações diárias atindido.", "Tente novamente amanhã")
        # page.add(ft.Text("Limite de interações diárias atingido. Tente novamente amanhã.", color=CONFIG["COLOR_TEXT_IN_CONTAINER"], size=40))

def reset_vars():
    global nome_usuario
    global liga_selecionada
    global ano_selecionado
    global acertos
    global data
    global random_names
    global correct_answer
    global categoria_quiz
    global chave_correspondente
    global url_liga
    global caminho_arquivo
    global categoria_atual
    nome_usuario = ""
    liga_selecionada = ""
    ano_selecionado = ""
    acertos = 0
    data = {}
    random_names = []
    correct_answer = ""
    categoria_quiz = ""
    chave_correspondente = ""
    url_liga = ""
    nome_usuario = ""
    liga_selecionada = ""
    ano_selecionado = ""
    caminho_arquivo = ''
    categoria_atual = 0

def configurar_pagina(page: ft.Page):
    page.title = 'QUIZ - CHUTE CERTEIRO'
    page.bgcolor = ft.colors.BLACK
    page.theme_mode = "white"
    page.window_maximized = True
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO
    page.clean()

def criar_menu(texto1, texto2=""):
    return ft.Container(
        col={'xs': 12, 'md': 6},
        bgcolor="#7586a4",
        padding=ft.padding.all(0),
        aspect_ratio=9/16,
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Row(alignment="center", controls=[ft.Text(value=texto1, size=35, color=CONFIG["COLOR_TEXT_IN_CONTAINER"])]),
                ft.Row(alignment="center", controls=[ft.Text(value=texto2, size=35, color=CONFIG["COLOR_TEXT_IN_CONTAINER"])]),
                ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[ft.Image(src="/images/logo.png", width=245, height=245)])
            ]
        )
    )

def criar_container_conteudo(conteudo):
    return ft.Container(
        col={'xs': 12, 'md': 6},
        bgcolor=ft.colors.WHITE,
        padding=ft.padding.all(0),
        aspect_ratio=9/16,
        content=ft.Column(alignment=ft.MainAxisAlignment.CENTER, controls=conteudo)
    )

def solicitar_nome(page: ft.Page, *_):
    def btn_click(e):
        if not txt_name.value:
            txt_name.error_text = "Por favor insira seu nome!"
            page.update()
        else:
            global nome_usuario
            nome_usuario = txt_name.value.title().strip()
            mostrar_ligas(page)

    txt_name = ft.TextField(
        label="Seu nome!", text_align='center', width=245, color=CONFIG["COLOR_TEXT"], cursor_color=CONFIG["COLOR_TEXT"],
        hint_style=ft.TextStyle(size=18, color=CONFIG["COLOR_TEXT"])
    )

    nome = criar_container_conteudo([
        ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[ft.Container(txt_name)]),
        ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[ft.Container(ft.ElevatedButton(text='Confirmar', content=ft.Text(value='Confirmar', size=30, color=CONFIG["COLOR_TEXT_IN_BUTTON"]), on_click=btn_click, width=CONFIG["SIZE_BUTTON"]))])
    ])

    layout = ft.Container(
        width=1000,
        margin=ft.margin.all(5),
        shadow=ft.BoxShadow(blur_radius=245, color=ft.colors.WHITE),
        content=ft.ResponsiveRow(columns=12, spacing=0, run_spacing=0, controls=[criar_menu("QUIZ", "CHUTE CERTEIRO"), nome])
    )
    page.add(layout)
    page.update()

def mostrar_ligas(page: ft.Page):
    page.clean()
    def on_button_click(e, liga_id):
        global liga_selecionada
        liga_selecionada = liga_id
        mostrar_anos(page)

    botoes_liga = [
        ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[
            ft.Container(
                ft.ElevatedButton(content=ft.Row([ft.Image(src=dados_liga['URL'], width=40, height=40), ft.Text(value=nome_liga, size=30, color=CONFIG["COLOR_TEXT_IN_BUTTON"])]),
                                on_click=lambda e, liga_id=dados_liga["ID"]: on_button_click(e, liga_id), width=CONFIG["SIZE_BUTTON"]))
        ])
        for nome_liga, dados_liga in ligas.items()
    ]

    escolhe_campeonato = criar_container_conteudo(botoes_liga)
    layout = ft.Container(
        width=1000,
        margin=ft.margin.all(5),
        shadow=ft.BoxShadow(blur_radius=245, color=ft.colors.WHITE),
        content=ft.ResponsiveRow(alignment=ft.MainAxisAlignment.CENTER, columns=12, spacing=0, run_spacing=0, controls=[criar_menu("ESCOLHA O", "CAMPEONATO"), escolhe_campeonato])
    )
    page.add(layout)
    page.update()

def mostrar_anos(page: ft.Page):
    page.clean()
    def on_button_click(e, ano):
        global ano_selecionado
        ano_selecionado = ano
        start_quiz(page, categorias[categoria_atual])

    botoes_ano = [
        ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[
            ft.Container(
                ft.ElevatedButton(content=ft.Text(value=ano, size=30, color=CONFIG["COLOR_TEXT_IN_BUTTON"], text_align='center'), on_click=lambda e, a=ano: on_button_click(e, a), width=CONFIG["SIZE_BUTTON"]))
        ])
        for ano in range(2016, 2024)
    ]

    escolhe_ano = criar_container_conteudo(botoes_ano)
    layout = ft.Container(
        width=1000,
        margin=ft.margin.all(5),
        shadow=ft.BoxShadow(blur_radius=245, color=ft.colors.WHITE),
        content=ft.ResponsiveRow(alignment=ft.MainAxisAlignment.CENTER, columns=12, spacing=0, run_spacing=0, controls=[criar_menu("ESCOLHA O ANO"), escolhe_ano])
    )
    page.add(layout)
    page.update()

def start_quiz(page: ft.Page, category):
    global categoria_quiz
    categoria_quiz = str(category)
    page.clean()
    if verificar_interacoes():
        api_futebol()
        global correct_answer, random_names
        correct_answer, random_names = generate_quiz(category)
        verificar_liga()
        mostrar_quiz(page)
    else:
        page.add(ft.Text("Limite de interações diárias atingido. Tente novamente amanhã.", color=CONFIG["COLOR_TEXT_IN_CONTAINER"], size=40))

def verificar_interacoes():
    if not os.path.exists(caminho_arquivo):
        with open(caminho_arquivo, 'w') as arquivo:
            arquivo.write("1")
        return True
    with open(caminho_arquivo, 'r') as arquivo:
        interacoes = int(arquivo.read().strip())
    if interacoes < max_interacoes:
        with open(caminho_arquivo, 'w') as arquivo:
            arquivo.write(str(interacoes + 1))
        return True
    return False

def verificar_arquivo_interacoes():
    global caminho_arquivo
    hoje = datetime.datetime.now().strftime("%Y-%m-%d")
    diretorio_log = os.path.join("assets", "log")
    if not os.path.exists(diretorio_log):
        os.makedirs(diretorio_log)
    caminho_arquivo = os.path.join(diretorio_log, f"interacoes_{hoje}.txt")

def interacoes_restantes():
    if not os.path.exists(caminho_arquivo):
        return True
    with open(caminho_arquivo, 'r') as arquivo:
        interacoes = int(arquivo.read().strip())
    return interacoes < max_interacoes

def api_futebol():
    global data
    busca_api = {
        'artilheiro': 'topscorers',
        'assistências': 'topassists',
        'cartões': 'topyellowcards'
    }[categoria_quiz]
    
    url = f"https://api-football-v1.p.rapidapi.com/v3/players/{busca_api}"
    querystring = {"league": str(liga_selecionada), "season": str(ano_selecionado)}
    headers = ler_keys_api(nome_arquivo_keys)

    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code != 200:
        print(f"Erro na requisição: {response.status_code}")
        return

    data = response.json()
    if 'response' not in data:
        print("Dados esperados não estão presentes na resposta da API")
        return

def generate_quiz(category):
    all_players = data['response']

    for player in all_players:
        if 'player' not in player or 'name' not in player['player']:
            print("Dados do jogador estão ausentes ou incompletos")
            return

    if category == 'artilheiro':
        all_names = [(player['player']['name'], player['statistics'][0]['goals']['total']) for player in all_players]
    elif category == 'assistências':
        all_names = [(player['player']['name'], player['statistics'][0]['goals']['assists']) for player in all_players]
    else:
        all_names = [(player['player']['name'], player['statistics'][0]['cards']['yellow']) for player in all_players]

    all_names.sort(key=lambda x: x[1], reverse=True)
    correct_name = all_names[0][0]
    global random_names
    random_names = random.sample([player['player']['name'] for player in all_players], 4)
    if correct_name not in random_names:
        random_names.pop()
        random_names.append(correct_name)
    random.shuffle(random_names)
    return correct_name, random_names

def verificar_liga():
    global chave_correspondente, url_liga
    for liga, info in ligas.items():
        if info["ID"] == liga_selecionada:
            chave_correspondente = liga
            url_liga = info['URL']
            break
    else:
        chave_correspondente = 'Não encontrada'

def texto_tela(page: ft.Page, imagem: bool, texto: str, *_: str):
        page.clean()
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.scroll = ft.Page.scroll
        if imagem:
            page.add(ft.Image(src="/images/logo.png", height=245, width=245))
        layout = ft.Container(content=ft.Text(texto, color=CONFIG["COLOR_TEXT_IN_CONTAINER"], size=40))
        page.add(layout)
        for resto in _:
            page.add(ft.Container(content=ft.Text(resto, color=CONFIG["COLOR_TEXT_IN_CONTAINER"], size=40)))

def check_answer(page: ft.Page, user_choice, correct_answer):
    global categoria_atual, acertos
    page.clean()
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    texto_tela(page, True, "Verificando sua resposta aguarde!")
    time.sleep(2)
    page.clean()

    if user_choice == correct_answer:
        acertos += 1
        texto_tela(page, False, "Sua resposta está correta!")
    else:
        texto_tela(page, False, f"Sua resposta está incorreta! A resposta era {correct_answer}!")
    
    time.sleep(2)
    categoria_atual += 1
    if categoria_atual < len(categorias):
        start_quiz(page, categorias[categoria_atual])
    else:
        finalizar_quiz(page)

# def texto_tela(page: ft.Page, imagem: bool, texto: str, *_: str):
#     page.clean()
#     page.vertical_alignment = ft.MainAxisAlignment.CENTER
#     page.horizontal_alignment = ft.MainAxisAlignment.CENTER
#     page.scroll = ft.Page.scroll
#     if imagem:
#         page.add(ft.Image(src="/images/logo.png", height=245, width=245))
#     page.add(ft.Text(texto, color=CONFIG["COLOR_TEXT_IN_CONTAINER"], size=40))
#     for r in _:
#         page.add(ft.Text(r, color=CONFIG["COLOR_TEXT_IN_CONTAINER"], size=40))


def finalizar_quiz(page: ft.Page):
    page.clean()
    texto1 = "Fim do Quiz!"
    texto2 = "Você respondeu todas as categorias"
    if acertos > 1:
        texto3 = f"Parabéns {nome_usuario} você acertou {acertos} de {len(categorias)} questões"
    else:
        texto3 = f"{nome_usuario} você acertou {acertos} de {len(categorias)} questões"
    
    texto_tela(page, True, texto1, texto2, texto3)
    
    time.sleep(5)
    main(page)

def mostrar_quiz(page: ft.Page):
    def on_button_click(e, jogador):
        global jogador_selecionado
        jogador_selecionado = jogador
        confirmacao(page)

    page.clean()
    page.scroll = ft.ScrollMode.AUTO
    if categoria_quiz == 'artilheiro':
        texto_quiz = f'Artilheiro de {ano_selecionado}?'
        texto_quiz2 = ""
    elif categoria_quiz == 'assistências':
        texto_quiz = f'Lider de assistências'
        texto_quiz2 = f' de {ano_selecionado}?'
    else:
        texto_quiz = f'Lider de cartões '
        texto_quiz2 = f'amarelos de {ano_selecionado}?'

    botoes_jogador = [
        ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[
            ft.Container(
                ft.ElevatedButton(content=ft.Row([ft.Image(src=player['player']['photo'], width=50, height=50), ft.Text(player['player']['name'], size=25, color=CONFIG["COLOR_TEXT_IN_BUTTON"])]),
                                on_click=lambda e, jogador=player['player']['name']: on_button_click(e, jogador), width=CONFIG["SIZE_BUTTON"], height=100))
        ])
        for player in data['response'] if player['player']['name'] in random_names
    ]

    escolhe_jogador = criar_container_conteudo(botoes_jogador)
    layout = ft.Container(
        width=1000,
        margin=ft.margin.all(5),
        shadow=ft.BoxShadow(blur_radius=245, color=ft.colors.WHITE),
        content=ft.ResponsiveRow(alignment=ft.MainAxisAlignment.CENTER, columns=12, spacing=0, run_spacing=0, controls=[criar_menu(texto_quiz, texto_quiz2), escolhe_jogador])
    )
    page.add(layout)
    page.update()

def confirmacao(page: ft.Page):
    def retorna_quiz(e):
        mostrar_quiz(page)

    def confirmado(e):
        check_answer(page, jogador_selecionado, correct_answer)

    page.clean()

    menu = criar_menu("VOCÊ TEM CERTEZA", "DA SUA RESPOSTA ?")
    confirmacao_botoes = criar_container_conteudo([
        ft.Row([
            ft.ElevatedButton(content=ft.Text(value='Sim', size=30, color=CONFIG["COLOR_TEXT_IN_BUTTON"]), on_click=confirmado, width=CONFIG["SIZE_BUTTON_CONFIRM"]),
            ft.ElevatedButton(content=ft.Text(value='Não', size=30, color=CONFIG["COLOR_TEXT_IN_BUTTON"]), on_click=retorna_quiz, width=CONFIG["SIZE_BUTTON_CONFIRM"])
        ], alignment=ft.MainAxisAlignment.CENTER)
    ])

    layout = ft.Container(
        width=1000,
        margin=ft.margin.all(5),
        shadow=ft.BoxShadow(blur_radius=245, color=ft.colors.WHITE),
        content=ft.ResponsiveRow(alignment=ft.MainAxisAlignment.CENTER, columns=12, spacing=0, run_spacing=0, controls=[menu, confirmacao_botoes])
    )
    page.add(layout)
    page.update()

def ler_keys_api(caminho_arquivo):
    try:
        with open(caminho_arquivo, 'r', encoding='utf8') as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        print('Arquivo não encontrado')
        return {}
    
if __name__ == "__main__":
    flet_path = os.getenv("FLET_PATH")  
    ft.app(target=main, assets_dir="assets", port=8080, view=ft.AppView.WEB_BROWSER, name=flet_path)
