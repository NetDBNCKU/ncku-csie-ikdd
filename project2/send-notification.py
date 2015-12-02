import requests
import json
from bs4 import BeautifulSoup

def send_index_notification(email, what, index):
    return requests.post(
        "https://api.mailgun.net/v3/sandboxb5dfc8d5d9534b8782012f37a539ae40.mailgun.org/messages",
        auth=("api", "key-5089c55c89423da3b648cdd9d5fc359e"),
        data={"from": "Mailgun Sandbox <postmaster@sandboxb5dfc8d5d9534b8782012f37a539ae40.mailgun.org>",
              "to": email,
              "subject": "Index notify",
              "text": "Congratulations! Your stock(" + what + "): " + str(index)})

registered_json = requests.get('https://vast-ridge-9264.herokuapp.com/load_registered_data').text
members = json.loads(registered_json)

page_source = requests.get('https://tw.stock.yahoo.com/us/worldidx.php')
soup = BeautifulSoup(page_source.text, 'html5lib')

for tr in soup.select('table[cellpadding="4"] tr'):
    if len(tr.attrs) == 0:
        pass
    elif tr.attrs['bgcolor'] == 'white':
        what, index = tr.select('a')[0].text, float(tr.select('b')[0].text)
        for member in members:
            if member['what'] in what:
                if index > member['lower'] and index < member['upper']:
                    print('Success: ' + str(member['lower']) + ' < ' + str(index) + ' < ' + str(member['upper']))
                    send_index_notification(email=member['email'], what=member['what'], index=index)
                else:
                    print('Failed: ' + str(index) + ' is not in range(' + str(member['lower']) + ', ' + str(member['upper']) + ')')
