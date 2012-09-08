from django.contrib.auth.models import User
from django.db import models
from django.conf import settings

class Summoner(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=40)
    level = models.IntegerField()
    wins = models.IntegerField()
    losses = models.IntegerField()
    leaves = models.IntegerField()

    def __unicode__(self):
        return "%s (%s)" % (self.name, self.level)

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
    owner = models.ForeignKey(User)
    players = models.ManyToManyField(Summoner, through='Game_Player')
    match_type = models.IntegerField()
    game_mode = models.IntegerField()
    queue_type = models.CharField(max_length=20)
    region = models.CharField(max_length=20)
    ranked = models.BooleanField()
    winning_team = models.IntegerField()
    match_length = models.IntegerField() #in seconds

    def __unicode__(self):
        return "%s: %ss (%s)" % (self.queue_type, self.match_length, self.region)

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
        return "%s (%s) - %s" % (self.player.name, self.champion.name, self.game.queue_type)
