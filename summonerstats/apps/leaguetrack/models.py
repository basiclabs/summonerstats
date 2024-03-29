from django.contrib.auth.models import User
from django.db import models
from django.db.models import Count
from django.conf import settings
from django.template.defaultfilters import slugify
from datetime import datetime

class Summoner(models.Model):
    followers = models.ManyToManyField(User, blank=True, null=True)
    name = models.CharField(max_length=40)
    level = models.IntegerField(default=1)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    leaves = models.IntegerField(default=0)
    region = models.CharField(max_length=20)
    slug_name = models.SlugField(unique=True)

    def __unicode__(self):
        return "%s (%s)" % (self.name, self.level)

    def total_games(self):
        return self.wins + self.losses + self.leaves

    def win_ratio(self):
        return "%s%%" % int(float(self.wins) / float(self.total_games()) * 100)

    def href(self):
        return "/summoner/%s/%s/" % (self.region, slugify(self.name))

    def favorite_champion(self):
        return Champion.objects.filter(game_player__player=self)\
            .annotate(num_plays=Count('pk'))\
            .order_by('-num_plays')[0]

class Champion(models.Model):
    name = models.CharField(max_length=40)
    title = models.CharField(max_length=100)
    reference = models.IntegerField()

    def __unicode__(self):
        return "%s (%s)" % (self.full_name(), self.reference)

    def portrait_url(self, size=120):
        return "%simg/champions/%s/%s.png" % (settings.STATIC_URL, size, self.slug_name())

    def slug_name(self):
        return self.name.replace("'", "").replace(" ", "").replace(".", "").lower()

    def full_name(self):
        return "%s, %s" % (self.name, self.title)

class Game(models.Model):
    uploader = models.ForeignKey(User)
    players = models.ManyToManyField(Summoner, through='Game_Player')
    match_type = models.IntegerField()
    game_mode = models.IntegerField()
    queue_type = models.CharField(max_length=20)
    region = models.CharField(max_length=20)
    ranked = models.BooleanField()
    winning_team = models.IntegerField()
    match_length = models.IntegerField() #in seconds
    timestamp = models.DateTimeField()
    upload_timestamp = models.DateTimeField(default=datetime.now())

    class Meta:
        ordering = ['-upload_timestamp']

    def __unicode__(self):
        return "%s; %s; %s; %ss" % (self.uploader, self.queue_type, self.region.upper(), self.match_length)

    def href(self):
        return '/game/%s' % self.pk

    def game_players(self):
        return Game_Player.objects.filter(game=self)

    def team1(self):
        return Game_Player.objects.filter(game=self, team=1)

    def team2(self):
        return Game_Player.objects.filter(game=self, team=2)

    def get_favorites(self, fave_list):
        def list_contains(l, item):
            for l_item in l:
	        if l_item.name == item.name:
                    return True
            return False
    
        return [player for player in self.players.all().order_by('pk') if list_contains(fave_list, player)]

class SummonerSpell(models.Model):
    name = models.CharField(max_length=40)
    description = models.TextField()
    required_level = models.IntegerField()
    cooldown = models.IntegerField()
    bonus_cooldown = models.IntegerField()

    def __unicode__(self):
        return self.name

class Item(models.Model):
    reference = models.IntegerField()
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    reduced_price = models.IntegerField(blank=True, null=True)
    effect = models.TextField()
    built_from = models.ManyToManyField("self", symmetrical=False, blank=True)

    def __unicode__(self):
        return self.name

class Game_Player(models.Model):
    game = models.ForeignKey(Game)
    player = models.ForeignKey(Summoner)

    team = models.IntegerField()
    champion = models.ForeignKey(Champion)
    level = models.IntegerField()
    kills = models.IntegerField()
    deaths = models.IntegerField()
    assists = models.IntegerField()
    damage_dealt = models.IntegerField()
    damage_taken = models.IntegerField()
    gold = models.IntegerField()
    creep_score = models.IntegerField()
    summoner_level = models.IntegerField()
    neutral_minions = models.IntegerField()
    healed = models.IntegerField()
    largest_multikill = models.IntegerField()
    magic_damage_taken = models.IntegerField()
    killing_spree = models.IntegerField()
    magic_damage_dealt = models.IntegerField()
    physical_damage_dealt = models.IntegerField()
    turrets = models.IntegerField()
    barracks = models.IntegerField()
    physical_damage_taken = models.IntegerField()
    time_dead = models.IntegerField()
    items = models.ManyToManyField(Item)
    summoner_spells = models.ManyToManyField(SummonerSpell)
    wins = models.IntegerField()
    losses = models.IntegerField()
    leaves = models.IntegerField()

    def __unicode__(self):
        return "%s -- %s (%s)" % (self.game, self.player.name, self.champion.name)
