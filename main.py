import time
from playsound import playsound

from apirequests.stratz import get_heroes_list
from overlay.configoverlay import start_overlay_config


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


heroes_list = get_heroes_list()


def get_hero_id(hero_name):
   return list(filter(lambda x: x[1]['displayName'] == hero_name, heroes_list.items()))[0][1]['id']


# MEDUSA
carry = get_hero_id('Anti-Mage')
# SILENCER
mid = get_hero_id('Silencer')
# PUDGE
off = get_hero_id('Alchemist')
# SK
sup4 = get_hero_id('Witch Doctor')
# DISRUPTOR
sup5 = get_hero_id('Mirana')

start_overlay_config(get_hero_id('Medusa'),
                     [886742476, 106573901, 193564777, 176155470, 194979527, 392565237, 375507918, 293731272, 898754153, 172099728, 97658618,
                      177411785, 110583422, 320252024, 113995822, 26316691, 315657960, 165390194, 127617979, 114619230, 132309493,
                      61049916, 245373129, 132851371, 1171243748, 81475303, 321580662, 86745912, 206642367, 181716137,
                      100058342, 122049498, 162610516, 111114687, 141690233, 196442862, 167976729, 148215639, 116934015, 155162307],
                     [carry, mid, off, sup4, sup5])
