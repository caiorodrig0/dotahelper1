import datetime

import requests
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


def search_match(player_id, hero_id):
    response = requests.get(f"{BASE_URL}/player/{player_id}/matches?take=30", headers=headers,
                            verify=False)
    matches = response.json()

    for match in matches:
        for hero_match in match["players"]:
            if hero_match["steamAccountId"] == player_id:
                if hero_match["heroId"] == hero_id:
                    return get_items_per_time(match['id'], player_id)


def check_if_core(_item):
    for item in core_items:
        if _item == item:
            return item


def format_text_to_display(items_n_timing):
    formated_items = ''
    for index, item in enumerate(items_n_timing):
        if index % 2 == 0 and item != '':
            formated_items += item + " - "

        elif item != '':
            formated_items += item + ' \n'

    return formated_items


def get_items_per_time(matchid, playerid):
    responsematch = requests.get(f"{BASE_URL}/match/{matchid}/breakdown", headers=headers, verify=False)
    data = responsematch.json()
    items_n_timing = ()
    for players in data['players']:
        if players['steamAccountId'] == playerid:
            for items in players['stats']['itemPurchases']:
                if check_if_core(get_name_by_id(items['itemId'])):
                    items_n_timing += (str(datetime.timedelta(seconds=items['time'])), get_name_by_id(items['itemId']))
            return format_text_to_display(items_n_timing)


def get_name_by_id(search_id):
    return item_data[str(search_id)]['displayName']
