import requests
import json
import sqlite3
from bs4 import BeautifulSoup

head = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:42.0) Gecko/20100101 Firefox/42.0'
}
platforms = (
    'psv', '3ds', 'psp', 'ps4', 'ps3', 'xboxone', 'xbox360',
    'wiiu', 'wii', 'nds', 'gba', 'ps', 'pc'
)
game = {}
session = requests.Session()
conn = sqlite3.connect('game.db')
curs = conn.cursor()

curs.execute('''CREATE TABLE game
                    (platform TEXT, name TEXT PRIMARY KEY, time TEXT,
                    type TEXT, view INTEGER, versions TEXT)''')

for platform in platforms:
    cur_page = 1
    while cur_page > 0:
        try:
            page_source = requests.get('http://tvgdb.duowan.com/' + platform + '?page=' + str(cur_page), timeout=10)
            soup = BeautifulSoup(page_source.text.encode(page_source.encoding).decode('utf8'), 'html5lib')
        except Exception as e:
            print('Crawl error({0}): {1}'.format(e.errno, e.strerror))
        else:
            print('PAGE GOT: ' + 'http://tvgdb.duowan.com/' + platform + '?page=' + str(cur_page))
        for item in soup.select('div.item'):
            try:
                game['platform'] = platform
                game['name'] = item.select('dd > ul > li > b')[0].text
                game['time'] = item.select('dd > ul > li > b')[3].text
                game['type'] = item.select('dd > ul > li > b')[5].text
                game['view'] = int(item.select('dd > ul > li > b')[10].text)
                is_version_label = True
                versions = []
                for version in item.select('div.version > span'):
                    if is_version_label:
                        is_version_label = False
                    else:
                        versions.append(version.text.strip())
                game['versions'] = '|'.join(versions)
            except Exception as e:
                print('Parse error({0}): {1}'.format(e.errno, e.strerror))
            else:
                print(game)
            try:
                curs.execute('INSERT OR IGNORE INTO game VALUES(' +
                        repr(game['platform']) + ', ' +
                        repr(game['name']) + ', ' +
                        repr(game['time']) + ', ' +
                        repr(game['type']) + ', ' +
                        repr(0) + ', ' +
                        repr(game['versions']) + ')')
                curs.execute('UPDATE game SET view = view + ' +
                        repr(game['view']) + ' WHERE name LIKE' +
                        repr(game['name']))
                conn.commit()
            except Exception as e:
                print('Insert error({0}): {1}'.format(e.errno, e.strerror))
            else:
                print('GAME INSERTED: ' + game['name'])
        cur_page += 1
        if len(soup.select('a.next.hidden')) > 0:
            cur_page = 0
conn.close()
