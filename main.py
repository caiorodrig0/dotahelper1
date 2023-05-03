import time

import requests

from apirequests.stratz import get_heroes_list
from overlay.configoverlay import start_overlay_config

heroes_list = get_heroes_list()


def get_hero_id(hero_name):
    return list(filter(lambda x: x[1]['displayName'] == hero_name, heroes_list.items()))[0][1]['id']


# MEDUSA
carry = get_hero_id('Faceless Void')
# SILENCER
mid = get_hero_id('Outworld Destroyer')
# PUDGE
off = get_hero_id('Bristleback')
# SK
sup4 = get_hero_id('Nyx Assassin')
# DISRUPTOR
sup5 = get_hero_id('Witch Doctor')


def get_players_id():
    response = requests.get('https://api.opendota.com/api/proPlayers', verify=False)

    if response.status_code == 200:
        pro_players = response.json()
        player_ids = [player['account_id'] for player in pro_players]
        return player_ids
    else:
        print(f"Erro na solicitação: {response.status_code}")


start_overlay_config(get_hero_id('Medusa'),
                     get_players_id(),
                     [carry, mid, off, sup4, sup5])
