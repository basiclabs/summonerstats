# Create your views here.
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from leaguetrack.models import *
from leaguetrack.utils import replay_from_url
import lolreader
from datetime import datetime

def home_page(request):
    if request.user.is_authenticated():
        return render(request, 'dashboard.html', {'owner': request.user})
    else:
        return render(request, 'base.html')

def view_metrics(request, region, summoner_name):
    summoner = Summoner.objects.get(region=region, name=summoner_name)
    return render(request, 'metrics.html', {'summoner': summoner})

def view_summoner(request, region, summoner_name):
    summoner = Summoner.objects.get(region=region, name=summoner_name)
    return render(request, 'summoner.html', {'summoner': summoner})

def view_game(request, game_id):
    game = Game.objects.get(pk=game_id)
    return render(request, 'game.html', {'game': game})

@login_required
def import_replay(request):
    url = request.GET.get('url', '')
    owner = request.user
    return render(request, 'base.html', {'rendertext': replay_from_url(owner, url)})
