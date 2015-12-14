import requests
import time
import json
import re

FIREBASE_HOST = 'burning-fire-3884.firebaseio.com'

if __name__ == '__main__':

    s = requests.Session()
    res = s.get('https://' + FIREBASE_HOST + '/new_game/.json')
    games = json.loads(res.text)
    game_arr = []
    minimal = 3000000
    maximal = -1
    earliest = 1500000000
    latest = 0 

    for game in games:
        if re.search(r'(19|20)\d{2}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])', games[game]['time']):
            t = time.strptime(games[game]['time'], '%Y-%m-%d')
            games[game]['time'] = int(time.mktime(t))
            games[game]['name'] = game
            game_arr.append(games[game])
            if games[game]['view'] > maximal:
                maximal = games[game]['view']
            if games[game]['view'] < minimal:
                minimal = games[game]['view']
            if games[game]['time'] > latest:
                latest = games[game]['time']
            if games[game]['time'] < earliest:
                earliest = games[game]['time']
                print(game)

    print('Minimal: ' + str(minimal))
    print('Maximal: ' + str(maximal))
    print('Earliest: ' + str(earliest))
    print('Latest: ' + str(latest))

    res = s.put('https://' + FIREBASE_HOST + '/game/.json', data=json.dumps(game_arr))
    print(res)
