# Create your views here.
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Q
from leaguetrack.models import *
from leaguetrack.utils import replay_from_url
import lolreader
from datetime import datetime

def home_page(request):
    if request.user.is_authenticated():
        user = request.user
        q = Q()
        for summoner in user.summoner_set.all():
            q |= Q(players__name = summoner.name)
        game_list = Game.objects.filter(q).distinct().order_by('-upload_timestamp')

        feedlist = []
        for game in game_list:
            feed_item = {'game': game, 'favorites': game.get_favorites(user.summoner_set.all()) }
            feedlist.append(feed_item)

        return render(request, 'dashboard.html', {'owner': request.user, 'feedlist': feedlist})
    else:
        return render(request, 'base.html')

def view_metrics(request, region, summoner_name):
    summoner = Summoner.objects.get(region__iexact=region, name__iexact=summoner_name)
    return render(request, 'metrics.html', {'summoner': summoner})

def view_summoner(request, region, summoner_name):
    summoner = Summoner.objects.get(region__iexact=region, name__iexact=summoner_name)
    summoner.followed = summoner.followers.filter(username=request.user.username).count() > 0
    return render(request, 'summoner.html', {'summoner': summoner})

@login_required
def follow_toggle_summoner(request, region, summoner_name):
    summoner = Summoner.objects.get(region__iexact=region, name__iexact=summoner_name)
    following = summoner.followers.filter(username=request.user.username).count() > 0
    if following:
        summoner.followers.remove(request.user)
    else:
        summoner.followers.add(request.user)
    summoner.save()
    return HttpResponse("success")

def view_game(request, game_id):
    game = Game.objects.get(pk=game_id)
    return render(request, 'game.html', {'game': game})

@login_required
def import_replay(request):
    url = request.GET.get('url', '')
    owner = request.user
    return render(request, 'base.html', {'rendertext': replay_from_url(owner, url)})
