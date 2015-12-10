import threading
import queue
import urllib.request
import urllib.error
import http.client
import html.parser
import sys
import re
from firebase import firebase
from bs4 import BeautifulSoup

VERSION_FLAG = {
    '中文版': 1,
    '美版': 2,
    '日版': 4,
    '欧版': 8,
    '国行版': 1,
    '英文版': 2,
    '硬盘版': 0
}

TYPE_FLAG = {
    '休闲益智类': 0,
    '体育类': 1,
    '其他类': 2,
    '冒险类': 3,
    '动作类': 4,
    '卡片类': 5,
    '即时战略类': 6,
    '射击类': 7,
    '文字类': 8,
    '格斗类': 9,
    '模拟类': 10,
    '竞速类': 11,
    '策略类': 12,
    '角色扮演类': 13,
    '音乐类': 14
}

PLATFORM_FLAG = {
    '3ds': 0,
    'gba': 1,
    'pc': 2,
    'ps': 3,
    'ps3': 4,
    'ps4': 5,
    'psp': 6,
    'psv': 7,
    'wii': 8,
    'wiiu': 9,
    'xbox360': 10,
    'xboxone': 11
}

MAX_SIZE_URL_QUEUE = 20
MAX_NUM_THREAD = 10
TIMEOUT_QUEUE = 60
TIMEOUT_REQUEST = 5

ref_queue = queue.Queue(MAX_SIZE_URL_QUEUE)
firebase = firebase.FirebaseApplication('https://burning-fire-3884.firebaseio.com', None)

def crawl():
    cont = True
    game = {}

    while cont:
        try:
            ref = ref_queue.get(timeout=TIMEOUT_QUEUE)
            url = 'http://tvgdb.duowan.com/' + ref['platform'] + '?page=' + str(ref['page'])
            try:
                response = urllib.request.urlopen(url, timeout=TIMEOUT_REQUEST)
            except Exception as e:
                print('Open exception')
                print(url)
                print(e)
            source = response.read().decode('utf8')
            soup = BeautifulSoup(source, 'html5lib')

            for item in soup.select('div.item'):
                try:
                    game_name = item.select('dd > ul > li > b')[0].text
                    game_name = game_name.replace('.', '')
                    if game_name.find('/') != -1:
                        game_name = game_name.replace('/', '(') + ')'
                    game['platform'] = PLATFORM_FLAG[ref['platform']]
                    game['time'] = item.select('dd > ul > li > b')[3].text
                    game['type'] = TYPE_FLAG[item.select('dd > ul > li > b')[5].text]
                    game['view'] = int(item.select('dd > ul > li > b')[10].text)
                    game['versions'] = 0
                    is_version_label = True
                    for version in item.select('div.version > span'):
                        if is_version_label:
                            is_version_label = False
                        else:
                            game['versions'] += VERSION_FLAG[version.text.strip()]

                    result = firebase.get('/game', game_name)
                    if result:
                        game['view'] += result['view']
                        firebase.put('/game', game_name, game)
                    else:
                        firebase.put('/game', game_name, game)
                except Exception as e:
                    print('Unknown item exception:')
                    print(url)
                    print(e)
        except queue.Empty:
            cont = False
            continue
        except http.client.HTTPException as e:
            print('Read exception:')
            print(url)
            print(e)
        except html.parser.HTMLParseError as e:
            print('Parse exception:')
            print(url)
            print(e)
        except Exception as e:
            print('Unknown page exception:')
            print(url)
            print(e)
        finally:
            sys.stdout.flush()
            ref_queue.task_done()

if __name__ == '__main__':

    for i in range(MAX_NUM_THREAD):
        t = threading.Thread(target=crawl, daemon=True)
        t.start()

    for platform in PLATFORM_FLAG:
        response = urllib.request.urlopen('http://tvgdb.duowan.com/' + platform)
        soup = BeautifulSoup(response.read().decode('utf8'), 'html5lib')
        href = soup.select('a.last')[0]['href']
        max_page = int(re.search('.*page=(\d+).*', href).group(1))
        for i in range(max_page):
            ref_queue.put({'platform': platform, 'page': i + 1})
