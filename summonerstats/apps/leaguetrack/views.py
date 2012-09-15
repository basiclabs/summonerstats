# Create your views here.
from django.http import HttpResponse, HttpRequest
from leaguetrack.models import *
import lolreader
from datetime import datetime

def home_page(request):
    if request.user.is_authenticated():
        #logged in!
        return HttpResponse("Welcome %s, <a href='/logout'>logout</a>." % request.user.username)
    else:
        #not logged in :(
        return HttpResponse("<a href='/login'>Login</a> or <a href='/register'>register</a>.")

def import_replay(request):
    url = request.GET.get('url', '')
    replay = lolreader.read_replay_from_url(url)
    
    winner = 1 if replay.teams[0].won else 2

    game_replay, game_created  = Game.objects.get_or_create(
        owner=User.objects.get(id=1),
        match_type=replay.match_type,
        game_mode=replay.game_mode,
        queue_type=replay.queue_type,
        region=replay.region,
        ranked=False,
        winning_team=winner,
        match_length=replay.match_length,
        timestamp=datetime.fromtimestamp(replay.timestamp)
    )

    summoners_added = champions_added = gps_added = 0

    for lolplayer in replay.players:
        summoner, summoner_created = Summoner.objects.get_or_create(
            user=User.objects.get(id=1),
            name=lolplayer.summoner,
            level=lolplayer.summoner_level,
            wins=lolplayer.wins,
            losses=lolplayer.losses,
            leaves=lolplayer.leaves
        )
        
        lol_champion, champion_created = Champion.objects.get_or_create(name=lolplayer.champion, title='the bullshitted', reference=1)

        gp, gp_created = Game_Player.objects.get_or_create(
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
            killing_spree=lolplayer.killing_spree,
            magic_damage_dealt=lolplayer.magic_damage_dealt,
            physical_damage_dealt=lolplayer.physical_damage_dealt,
            turrets=lolplayer.turrets,
            barracks=lolplayer.barracks,
            physical_damage_taken=lolplayer.physical_damage_taken,
            time_dead=lolplayer.time_dead,
            wins = lolplayer.wins,
            losses = lolplayer.losses,
            leaves = lolplayer.leaves
        )
        summoners_added = summoners_added + 1 if summoner_created else summoners_added
        champions_added = champions_added +1 if champion_created else champions_added
        gps_added = gps_added + 1 if gp_created else gps_added


    return HttpResponse("New Game? %s; Summoners Added: %s; Champions Added: %s; Game_Players Added: %s" % (game_created, summoners_added, champions_added, gps_added))
