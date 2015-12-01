from django.shortcuts import render
from django.http import HttpResponse
from .models import Member
import requests
from bs4 import BeautifulSoup
import json

# Create your views here.

def load_page(request):
    print(str(request));
    return render(request=request, template_name='index.html')

def register(request):
    Member.objects.create(
            email=request.GET['email'],
            what=request.GET['what'],
            lower=request.GET['lower'],
            upper=request.GET['upper'])
    return load_registerd_data(request)

def load_registerd_data(request):
    members = []
    for o in Member.objects.all():
        member = o.__dict__
        del member['_state']
        del member['timestamp']
        members.append(member)
    return HttpResponse(json.dumps(members))

def load_financial_data(request):
    page_source = requests.get('https://tw.stock.yahoo.com/us/worldidx.php')
    soup = BeautifulSoup(page_source.text, 'html5lib')
    what = []

    for tr in soup.select('table[cellpadding="4"] tr'):
        if len(tr.attrs) == 0:
            pass
        elif tr.attrs['bgcolor'] == 'white':
            what.append(tr.select('a')[0].text)

    return HttpResponse(json.dumps(what))
