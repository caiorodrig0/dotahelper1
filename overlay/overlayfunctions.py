
from apirequests.stratz import search_match, get_global_variables, get_items_per_time


def inicia_overlay(imagem_path, root, label, hero_id, players, heroes_against):
    regiao_busca = (580, 492, 62, 25)
    #posicao = pyautogui.locateOnScreen(imagem_path, region=regiao_busca, grayscale=True)
    posicao = 1
    if posicao:
        response_strataz = search_match(players, hero_id, heroes_against)
        while response_strataz is None and len(heroes_against) > 0:
            heroes_against.pop(-1)
            response_strataz = search_match(players, hero_id, heroes_against)

        #if response_strataz is not None:
            #label['text'] = response_strataz
        #else:
            #label['text'] = get_items_per_time(matchid=get_global_variables()[0]['id'], playerid=get_global_variables()[1])
    #else:
       # root.after(1, inicia_overlay(imagem_path, root, label, hero_id, players, heroes_against))
