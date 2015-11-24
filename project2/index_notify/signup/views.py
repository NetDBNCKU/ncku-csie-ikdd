from django.shortcuts import render
from django.http import HttpResponse
from bs4 import BeautifulSoup
import requests

# Create your views here.


def send_simple_message(request):

    page_source = requests.get('https://tw.stock.yahoo.com/us/worldidx.php')
    soup = BeautifulSoup(page_source.text, 'lxml')
    send = False

    for tr in soup.select('table[cellpadding="4"] tr'):
        if len(tr.attrs) == 0:
            pass
        elif tr.attrs['bgcolor'] == 'white':
            what, index = tr.select('a')[0].text, tr.select('b')[0].text
            if request.GET['what'] in what:
                if request.GET['operator'] == '<':
                    send = float(index) < float(request.GET['index'])
                elif request.GET['operator'] == '>':
                    send = float(index) > float(request.GET['index'])

    if send:
        return HttpResponse('Success!');
    else:
        return HttpResponse('Oops!');
