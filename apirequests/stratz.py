import datetime
import json

import requests

import apirequests.globalvariables
from apirequests import globalvariables
from apirequests.configstratz import BASE_URL, headers

responseitem = requests.get(f"{BASE_URL}/Item", headers=headers, verify=False)
item_data = responseitem.json()

core_items = ['Falcon Blade', 'Power Treads', 'Mask of Madness', 'Boots of Travel', 'Witch Blade',
              'Eul\'s Scepter of Divinity',
              'Orchid Malevolence', 'Aghanim\'s Scepter', 'Refresher Orb', 'Octarine Core', 'Scythe of Vyse',
              'Aghanim\'s Blessing',
              'Gleipnir, Wind Waker', 'Hood of Defiance', 'Blade Mail', 'Eternal Shroud', 'Lotus Orb', 'Black King Bar',
              'Bloodstone',
              'Hurricane Pike', 'Linken\'s Sphere', 'Manta Style', 'Shiva\'s Guard', 'Heart of Tarrasque',
              'Assault Cuirass',
              'Meteor Hammer', 'Armlet of Mordiggian', 'Skull Basher', 'Shadow Blade', 'Desolator', 'Battle Fury',
              'Nullifier',
              'Ethereal Blade', 'Radiance', 'Butterfly', 'Monkey King Bar', 'Daedalus', 'Silver Edge', 'Divine Rapier',
              'Revenant\'s Brooch', 'Abyssal Blade', 'Bloodthorn', 'Dragon Lance', 'Mage Slayer', 'Diffusal Blade',
              'Echo Sabre', 'Maelstrom', 'Heaven\'s Halberd', 'Kaya and Sange', 'Sange and Yasha', 'Yasha and Kaya',
              'Satanic', 'Eye of Skadi', 'Mjollnir', 'Arcane Blink', 'Overwhelming Blink', 'Swift Blink']


def check_if_heroes_in_the_match(match, hero_id, hero_against, player):
    heroes_found = list(
        filter(lambda x: x.get('isPick', True) and x.get('heroId') in hero_against and x.get('isRadiant') != player[
            'isRadiant'], match['pickBans']))

    if not player['isVictory']:
        return False

    if len(heroes_found) > globalvariables.heroes_found_global:
        globalvariables.heroes_found_global = len(heroes_found)
        globalvariables.best_match = match
        globalvariables.player_id_global = player['steamAccountId']

    if len(heroes_found) == 5 or len(hero_against) <= globalvariables.heroes_found_global:
        return True

    return False


def get_global_variables():
    return [globalvariables.best_match, globalvariables.heroes_found_global, globalvariables.player_id_global]


def get_heroes_list():
    response = requests.get(
        f"{BASE_URL}/Hero",
        headers=headers,
        verify=False)
    return response.json()


def search_match(players, hero_id, hero_against):
    for player_id in players:
        try:
            response = requests.get(
                f"{BASE_URL}/player/{player_id}/matches?take=100&heroId={hero_id}",
                headers=headers,
                verify=False)
            matches = response.json()
        except json.decoder.JSONDecodeError as e:
            print("Erro ao decodificar JSON: ", e)
            continue
        except requests.exceptions.RequestException as e:
            print("Erro na solicitação: ", e)
            continue

        for match in matches:
            if 'pickBans' in match and check_if_heroes_in_the_match(match, hero_id, hero_against,
                                                                    match['players'][0]):
                return get_items_per_time(apirequests.globalvariables.best_match['id'],
                                          apirequests.globalvariables.player_id_global)


def check_if_core(_item):
    for item in core_items:
        if _item == item:
            return item


def format_text_to_display(items_n_timing, match_id, date):
    formated_items = ''
    for index, item in enumerate(items_n_timing):
        if index % 2 == 0 and item != '':
            formated_items += item + " - "

        elif item != '':
            formated_items += item + ' \n'

    return formated_items + "\n\n\n\n" + "MatchID: " + str(match_id) + "\n\nData: " + str(
        datetime.datetime.fromtimestamp(date))


def get_items_per_time(matchid, playerid):
    responsematch = requests.get(f"{BASE_URL}/match/{matchid}/breakdown", headers=headers, verify=False)
    data = responsematch.json()
    items_n_timing = ()
    for players in data['players']:
        if players['steamAccountId'] == playerid:
            for items in players['stats']['itemPurchases']:
                if check_if_core(get_name_by_id(items['itemId'])):
                    items_n_timing += (str(datetime.timedelta(seconds=items['time'])), get_name_by_id(items['itemId']))
            return format_text_to_display(items_n_timing, matchid, data['startDateTime'])


def get_name_by_id(search_id):
    return item_data[str(search_id)]['displayName']
