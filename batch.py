import json

import firebase_admin
from firebase_admin import firestore, credentials
import datetime
import time
import requests

BASE_URL = "https://api.stratz.com/api/v1"

# Token de autenticação
token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1laWQiOiJodHRwczovL3N0ZWFtY29tbXVuaXR5LmNvbS9vcGVuaWQvaWQvNzY1NjExOTc5NzcyMzI2NDYiLCJ1bmlxdWVfbmFtZSI6IlQxIEZha2VyIiwiU3ViamVjdCI6IjY1MGJjYWJmLWMyNzctNGI3Ny04YTc5LTViMDc2NDJjMWY0ZiIsIlN0ZWFtSWQiOiIxNjk2NjkxOCIsIm5iZiI6MTY2OTY0MDY1MCwiZXhwIjoxNzAxMTc2NjUwLCJpYXQiOjE2Njk2NDA2NTAsImlzcyI6Imh0dHBzOi8vYXBpLnN0cmF0ei5jb20ifQ.OzPhHpmFd0QCFesHqDrPgQGmiOlwLx3bEBzlkirV-1o'

headers = {
    'Authorization': 'Bearer ' + token
}

cred = credentials.Certificate("firebase_key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
ten_days_ago = datetime.datetime.now() - datetime.timedelta(days=10)


def fill_matches(players, hero_id, use_cache=False):
    _matches = {}

    cache_keys = [f"{player_id}_{hero_id}" for player_id in players]
    if use_cache:
        docs = db.collection("matches").get()
        dic = list(filter(lambda x: f"_{hero_id}" in x['cache_key'], [doc.to_dict() for doc in docs]))
        _matches = {"matches": [doc["matches"] for doc in dic]}
    else:
        for cache_key in cache_keys:
            try:
                print("chamando o player: " + cache_key.split('_')[0])
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
                                               match["players"][0]["lane"] == 1 and
                                               datetime.datetime.fromtimestamp(match['startDateTime']) > ten_days_ago,
                                               matches))

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
                # doc_ref = db.collection("matches").document(cache_key)
                # doc_ref.set({"matches": []})
                print(f"Erro ao obter as partidas do jogador {cache_key.split('_')[0]}: {e}")

    return _matches


def get_players_id():
    response = requests.get('https://api.opendota.com/api/proPlayers', verify=False)

    if response.status_code == 200:
        pro_players = response.json()
        player_ids = [player['account_id'] for player in pro_players if
                      str(player['last_match_time']) > str(ten_days_ago)]
        return player_ids
    else:
        print(f"Erro na solicitação: {response.status_code}")


def get_hero_id(hero_name):
    return list(filter(lambda x: x[1]['displayName'] == hero_name, heroes_list.items()))[0][1]['id']


def get_heroes_list():
    response = requests.get(
        f"{BASE_URL}/Hero",
        headers=headers,
        verify=False)
    return response.json()


heroes_list = get_heroes_list()
main_heroes = ['Anti-Mage', 'Slark', 'Monkey King', 'Naga Siren', 'Riki', 'Faceless Void', 'Phantom Lancer'
    , 'Muerta', 'Bloodseeker', 'Sven', 'Templar Assassin', 'Medusa']

if __name__ == '__main__':
    print(f"Matches started at {datetime.datetime.now()}")
    for hero in main_heroes:
        print("************ Starting: " + hero + " ******************")
        success = False
        retry_count = 0
        while not success:
            try:
                fill_matches(players=get_players_id(), hero_id=get_hero_id(hero), use_cache=False)
                success = True
            except Exception as e:
                retry_count += 1
                if retry_count >= 5:
                    print(f"Tried 5 times without success. Waiting for 1 minute before trying again...")
                    time.sleep(60)
                    retry_count = 0
                else:
                    print(f"An exception occurred: {e}. Retrying in 10 seconds...")
                    time.sleep(10)

    print(f"Matches updated at {datetime.datetime.now()}")
