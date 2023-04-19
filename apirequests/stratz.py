import datetime

import requests
from apirequests.configstratz import BASE_URL, headers

responseitem = requests.get(f"{BASE_URL}/Item", headers=headers, verify=False)
item_data = responseitem.json()


def search_match(player_id, hero_id):
    response = requests.get(f"{BASE_URL}/player/{player_id}/matches?take=30", headers=headers,
                            verify=False)
    matches = response.json()

    for match in matches:
        for hero_match in match["players"]:
            if hero_match["steamAccountId"] == player_id:
                if hero_match["heroId"] == hero_id:
                    return get_items_per_time(match['id'], player_id)


def get_items_per_time(matchid, playerid):
    responsematch = requests.get(f"{BASE_URL}/match/{matchid}/breakdown", headers=headers, verify=False)
    data = responsematch.json()
    items_n_timing = ('', '')
    for players in data['players']:
        if players['steamAccountId'] == playerid:
            for items in players['stats']['itemPurchases']:
                items_n_timing += (str(datetime.timedelta(seconds=items['time'])), get_name_by_id(items['itemId']))
            return items_n_timing


def get_name_by_id(search_id):
    return item_data[str(search_id)]['displayName']
