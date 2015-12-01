import requests
from bs4 import BeautifulSoup

page_source = requests.get('https://tw.stock.yahoo.com/us/worldidx.php')
soup = BeautifulSoup(page_source.text, 'html5lib')

for tr in soup.select('table[cellpadding="4"] tr'):
    if len(tr.attrs) == 0:
        if len(tr.select('a')) == 0:
            print('%s\n\t%-40s\t%s' % (tr.select('font')[0].text, 'Name and Code', 'Index'))
    elif tr.attrs['bgcolor'] == 'white':
        print('\t%-40s\t%s' % (tr.select('a')[0].text, tr.select('b')[0].text))
