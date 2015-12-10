import sqlite3
from firebase import firebase

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

VERSION_FLAG = {
    '中文版': 1,
    '美版': 2,
    '日版': 4,
    '欧版': 8
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

if __name__ == '__main__':

    conn = sqlite3.connect('game.db')
    curs = conn.cursor()

    curs.execute('SELECT * FROM GAME')

    game = {}
    row = curs.fetchone()
    #firebase = firebase.FirebaseApplication('https://burning-fire-3884.firebaseio.com', None)
    t = 1
    while row:
        print(t)
        t += 1
        game_name = row[1]
        game['platform'] = PLATFORM_FLAG[row[0]]
        game['time'] = row[2]
        game['type'] = TYPE_FLAG[row[3]]
        game['view'] = row[4]
        game['versions'] = 0
        for version in row[5].split('|'):
            game['versions'] += VERSION_FLAG[version]
        try:
            #result = firebase.get('/game', game_name)
            #if result:
                #game['view'] += result['view']
                #firebase.put('/game', game_name, game)
            #else:
                #firebase.put('/game', game_name, game)
            pass
        except:
            pass
        row = curs.fetchone()
