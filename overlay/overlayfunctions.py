import pyautogui
from apirequests.stratz import search_match


def inicia_overlay(imagem_path, root, label, hero_id, player_id):
    regiao_busca = (580, 492, 62, 25)
    posicao = pyautogui.locateOnScreen(imagem_path, region=regiao_busca, grayscale=True)

    if posicao:
        # print(posicao)
        # label['text'] = '1 - Agrar creeps na lane (treinar esse conceito & last hit)\n2 - Farmar o little camp sempre ' \
        #                 'que possível e ir farmando a jungle na side lane\n3- Caso a lane esteja dificil e tenha o item ' \
        #                 'de farm, farmar ancient + lane do top\n4- Caso a primeira torre do top tiver caído, ' \
        #                 'farmar jungle do time inimigo, caso não, cogitar farmar propria jungle\n5- Wardar a jungle ' \
        #                 'inimiga'
        label['text'] = search_match(player_id, hero_id)
        # str(datetime.timedelta(seconds=items['time'])), get_name_by_id(items['itemId'])

    else:
        root.after(1, inicia_overlay(imagem_path, root, label, hero_id, player_id))
