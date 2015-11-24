from django.shortcuts import render
from django.http import HttpResponse
from bs4 import BeautifulSoup
import requests
import httplib2
import os
import argparse
import oauth2client
from oauth2client import tools
from oauth2client import client
from . import sendEmail
from apiclient import discovery

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
        message = sendEmail.CreateMessage(sender='rilislearning@gmail.com',
                to=request.GET['email'],
                subject='Index notify',
                message_text=(request.GET['what'] + ' is ' + request.GET['operator'] + ' ' + request.GET['index']))
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                       'gmail-python-quickstart.json')
        store = oauth2client.file.Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('gmail', 'v1', http=http)
        sendEmail.SendMessage(service=service, user_id='rilislearning@gmail.com', message=message)
        return HttpResponse('Success!');
    else:
        return HttpResponse('Oops!');
