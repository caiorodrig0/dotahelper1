import pyautogui
from apirequests.stratz import search_match


def inicia_overlay(imagem_path, root, label, hero_id, player_id, hero_against):
    regiao_busca = (580, 492, 62, 25)
    posicao = pyautogui.locateOnScreen(imagem_path, region=regiao_busca, grayscale=True)

    if posicao:
        label['text'] = search_match(player_id, hero_id, hero_against)
    else:
        root.after(1, inicia_overlay(imagem_path, root, label, hero_id, player_id, hero_against))
