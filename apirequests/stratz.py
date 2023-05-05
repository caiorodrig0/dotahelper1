import json

import firebase_admin
from firebase_admin import firestore, credentials
import datetime
import requests
import apirequests.globalvariables
from apirequests import globalvariables
from apirequests.configstratz import BASE_URL, headers

cred = credentials.Certificate("firebase_key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
responseitem = requests.get(f"{BASE_URL}/Item", headers=headers, verify=False)
item_data = responseitem.json()

ten_days_ago = datetime.datetime.now() - datetime.timedelta(days=10)

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


def check_if_heroes_in_the_match(match, hero_id, hero_against):
    heroes_found = list(
        filter(lambda x: x.get('isPick', True) and x.get('heroId') in hero_against and x.get('isRadiant') != match[
            'isRadiant'] and match['imp'] > 0, match['pickBans']))

    if not match['isVictory']:
        return False

    if len(heroes_found) > globalvariables.heroes_found_global:
        globalvariables.heroes_found_global = len(heroes_found)
        globalvariables.best_match = match
        globalvariables.player_id_global = match['steamAccountId']

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


def get_matches(player_id, hero_id):
    cache_key = f"{player_id}_{hero_id}"
    matches = list(filter(lambda x: x.get('cache_key') == cache_key, [d for sublist in apirequests.globalvariables.matches_cache['matches'] for d in sublist]))

    if matches is not None and len(matches) > 0:
        return matches
    return {}


def fill_matches(players, hero_id, use_cache):
    _matches = {}

    cache_keys = [f"{player_id}_{hero_id}" for player_id in players]
    if use_cache:
            docs = db.collection("matches").get()
            dic = list(filter(lambda x: f"_{hero_id}" in x['cache_key'], [doc.to_dict() for doc in docs]))
            _matches = {"matches": [doc["matches"] for doc in dic]}
    else:
        for cache_key in cache_keys:
            try:
                response = requests.get(
                    f"{BASE_URL}/player/{cache_key.split('_')[0]}/matches?take=100&heroId={hero_id}",
                    headers=headers,
                    verify=False
                )
                matches = response.json()
                filtered_matches = list(filter(lambda match:
                                               match.get("pickBans", []) != [] and
                                               match["players"][0].get("imp", 0) > 0 and
                                               match["players"][0]["isVictory"] and
                                               datetime.datetime.fromtimestamp(match['startDateTime']) > ten_days_ago, matches))

                filtered_matches = [{"id": match["id"],
                                     "cache_key": cache_key,
                                     "imp": match['players'][0]["imp"],
                                     "isVictory": match['players'][0]["isVictory"],
                                     "isRadiant": match['players'][0]["isRadiant"],
                                     "steamAccountId": match['players'][0]["steamAccountId"],
                                     "didRadiantWin": match["didRadiantWin"],
                                     "pickBans": match.get("pickBans", [])}
                                    for match in filtered_matches]

                if filtered_matches:
                    doc_ref = db.collection("matches").document(cache_key)
                    doc_ref.set({"matches": filtered_matches, "cache_key": cache_key})
                    _matches[cache_key] = filtered_matches

            except (json.decoder.JSONDecodeError, requests.exceptions.RequestException) as e:
                #doc_ref = db.collection("matches").document(cache_key)
                #doc_ref.set({"matches": []})
                print(f"Erro ao obter as partidas do jogador {cache_key.split('_')[0]}: {e}")

    return _matches


def search_match(players, hero_id, hero_against):
    apirequests.globalvariables.matches_cache = fill_matches(players, hero_id, False)
    for player_id in players:
        matches = get_matches(player_id, hero_id)
        for match in matches:
            if 'pickBans' in match and len(match['pickBans']) > 0 and check_if_heroes_in_the_match(match, hero_id, hero_against):
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
