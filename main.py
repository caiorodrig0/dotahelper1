import json
import tkinter as tk
import pyautogui
import time
from playsound import playsound
import requests
import datetime

BASE_URL = "https://api.stratz.com/api/v1"

# Token de autenticação
token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1laWQiOiJodHRwczovL3N0ZWFtY29tbXVuaXR5LmNvbS9vcGVuaWQvaWQvNzY1NjExOTc5NzcyMzI2NDYiLCJ1bmlxdWVfbmFtZSI6IlQxIEZha2VyIiwiU3ViamVjdCI6IjY1MGJjYWJmLWMyNzctNGI3Ny04YTc5LTViMDc2NDJjMWY0ZiIsIlN0ZWFtSWQiOiIxNjk2NjkxOCIsIm5iZiI6MTY2OTY0MDY1MCwiZXhwIjoxNzAxMTc2NjUwLCJpYXQiOjE2Njk2NDA2NTAsImlzcyI6Imh0dHBzOi8vYXBpLnN0cmF0ei5jb20ifQ.OzPhHpmFd0QCFesHqDrPgQGmiOlwLx3bEBzlkirV-1o'

headers = {
    'Authorization': 'Bearer ' + token
}

responseitem = requests.get(f"{BASE_URL}/Item", headers=headers, verify=False)
item_data = responseitem.json()

imagem_path = '5.png'
# Criar uma janela sem borda com background transparente
root = tk.Tk()
root.overrideredirect(True)
root.wait_visibility(root)
root.attributes('-alpha', 0.7)

# Criar um label com o texto "Olá, mundo!"
label = tk.Label(root, text="Aguardando jogo iniciar...", font=("Arial", 8), bg='white')
label.pack()

# Exibir a janela sempre no topo
root.lift()
root.attributes("-topmost", True)
root.geometry("+%d+%d" % (0, 300))


def printrelogio():
    tempo_inicial = time.time()

    # espera 1 segundo
    time.sleep(1)

    # obtém o tempo atual
    tempo_atual = time.time()

    # calcula o tempo que passou
    tempo_decorrido = tempo_atual - tempo_inicial

    if 50 < tempo_decorrido <= 59:
        playsound('count.mp3.mp3')
    elif tempo_decorrido == 60:
        tempo_decorrido = 0


printrelogio()


def findbuild():
    player_id = 345001363
    hero_id = 67
    response = requests.get(f"{BASE_URL}/player/{player_id}/matches?take=30", headers=headers, verify=False)
    matches = response.json()

    for match in matches:
        for hero_match in match["players"]:
            if hero_match["steamAccountId"] == player_id:
                if hero_match["heroId"] == hero_id:
                    getitemspertime(match['id'], player_id)
                    break


def get_name_by_id(search_id):
    return item_data[str(search_id)]['displayName']


def getitemspertime(matchid, playerid):
    responsematch = requests.get(f"{BASE_URL}/match/{matchid}/breakdown", headers=headers, verify=False)
    data = responsematch.json()

    for players in data['players']:
        if players['steamAccountId'] == playerid:
            for items in players['stats']['itemPurchases']:
                print(str(datetime.timedelta(seconds=items['time'])), get_name_by_id(items['itemId']))


def atualizar_contador():
    regiao_busca = (580, 492, 62, 25)
    posicao = pyautogui.locateOnScreen(imagem_path, region=regiao_busca, grayscale=True)

    if posicao:
        print(posicao)
        label['text'] = '1 - Agrar creeps na lane (treinar esse conceito & last hit)\n2 - Farmar o little camp sempre ' \
                        'que possível e ir farmando a jungle na side lane\n3- Caso a lane esteja dificil e tenha o item ' \
                        'de farm, farmar ancient + lane do top\n4- Caso a primeira torre do top tiver caído, ' \
                        'farmar jungle do time inimigo, caso não, cogitar farmar propria jungle\n5- Wardar a jungle ' \
                        'inimiga'
        # printrelogio()
        findbuild()
    else:
        label['text'] = 'Aguardando inicio do jogo...'
        root.after(1, atualizar_contador)


root.after(1, atualizar_contador)

# Iniciar o loop da janela
root.mainloop()
