import requests
import json
from firebase import firebase
from bs4 import BeautifulSoup

head = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:42.0) Gecko/20100101 Firefox/42.0'
}
platforms = (
    'psv', '3ds', 'psp', 'ps4', 'ps3', 'xboxone', 'xbox360',
    'wiiu', 'wii', 'nds', 'gba', 'ps', 'pc'
)
game = {}
game_name = ''
session = requests.Session()
firebase = firebase.FirebaseApplication('https://burning-fire-3884.firebaseio.com', None)

for platform in platforms:
    cur_page = 1
    while cur_page > 0:
        try:
            page_source = requests.get('http://tvgdb.duowan.com/' + platform + '?page=' + str(cur_page), timeout=10)
            soup = BeautifulSoup(page_source.text.encode(page_source.encoding).decode('utf8'), 'html5lib')
        except Exception as e:
            print('Crawl exception: ' + platform + ':' + str(cur_page))
        else:
            print('PAGE GOT: ' + 'http://tvgdb.duowan.com/' + platform + '?page=' + str(cur_page))
        for item in soup.select('div.item'):
            try:
                game_name = item.select('dd > ul > li > b')[0].text.replace('&', 'and')
                game['platform'] = platform
                game['time'] = item.select('dd > ul > li > b')[3].text
                game['type'] = item.select('dd > ul > li > b')[5].text
                game['view'] = int(item.select('dd > ul > li > b')[10].text)
                game['versions'] = []
                is_version_label = True
                for version in item.select('div.version > span'):
                    if is_version_label:
                        is_version_label = False
                    else:
                        game['versions'].append(version.text.strip())
            except Exception as e:
                print('Parse exception: ' + platform + ':' + str(cur_page))
            else:
                print(game)
            try:
                result = firebase.get('/game', game_name)
                if result:
                    game['view'] += result['view']
                    firebase.put('/game', game_name, game)
                else:
                    firebase.put('/game', game_name, game)
            except Exception as e:
                print('Insert exception: ' + platform + ':' + str(cur_page))
            else:
                print('GAME INSERTED: ' + game['name'])
        cur_page += 1
        if len(soup.select('a.next.hidden')) > 0:
            cur_page = 0
