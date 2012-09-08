# Create your views here.
from django.http import HttpResponse, HttpRequest
from leaguetrack.models import *
import lolreader
from datetime import datetime

def import_replay(request):
    url = request.GET.get('url', '')
    replay = lolreader.read_replay_from_url(url)

    owner = User(id=1)
    match_type = 1
    game_mode=1
    queue_type="Normal"
    region = "NA"
    ranked = False
    
    winner = 1 if replay.teams[0].won else 2

    game_replay, created  = Game.objects.get_or_create(
        owner=User.objects.get(id=1),
        match_type=1,
        game_mode=1,
        queue_type='Normal',
        region='NA',
        ranked=False,
        winning_team=winner,
        match_length=2200,
        timestamp=datetime(2012,8,7,12,0,0)
    )

    for lolplayer in replay.players:
        summoner, created = Summoner.objects.get_or_create(user=User.objects.get(id=1), name=lolplayer.summoner, level=lolplayer.summoner_level, wins=lolplayer.wins, losses=lolplayer.losses, leaves=lolplayer.leaves)
        lol_champion, created = Champion.objects.get_or_create(name=lolplayer.champion, title='the bullshitted', reference=1)
        gp = Game_Player(
            game=game_replay,
            player=summoner,
            team=lolplayer.team,
            champion = lol_champion,
            level = lolplayer.level,
            kills = lolplayer.kills,
            deaths=lolplayer.deaths,
            assists=lolplayer.assists,
            damage_dealt=lolplayer.damage_dealt,
            damage_taken=lolplayer.damage_taken,
            gold=lolplayer.gold,
            creep_score=lolplayer.minions,
            summoner_level=lolplayer.summoner_level,
            neutral_minions=lolplayer.neutral_minions_killed,
            healed=lolplayer.healed,
            largest_multikill=lolplayer.largest_multi_kill,
            magic_damage_taken=lolplayer.magic_damage_taken,
            killing_spree=0,
            magic_damage_dealt=lolplayer.magic_damage_dealt,
            physical_damage_dealt=lolplayer.physical_damage_dealt,
            turrets=0,
            barracks=0,
            physical_damage_taken=lolplayer.physical_damage_taken,
            time_dead=lolplayer.time_dead,
            wins = lolplayer.wins,
            losses = lolplayer.losses,
            leaves = lolplayer.leaves
        )
        gp.save()

    return HttpResponse(url)
