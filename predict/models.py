from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
import datetime
# Create your models here.


class Game(models.Model):
    CHOICES = (
        ('ATL', 'Atlanta Hawks'),
        ('BKN', 'Brooklyn Nets'),
        ('BOS', 'Boston Celtics'),
        ('CHA', 'Charlotte Hornets'),
        ('CHI', 'Chicago Bulls'),
        ('CLE', 'Cleveland Cavaliers'),
        ('DAL', 'Dallas Mavericks'),
        ('DEN', 'Denver Nuggets'),
        ('DET', 'Detroit Pistons'),
        ('GSW', 'Golden State Warriors'),
        ('HOU', 'Houston Rockets'),
        ('IND', 'Indiana Pacers'),
        ('LAC', 'Los Angeles Clippers'),
        ('LAL', 'Los Angeles Lakers'),
        ('MEM', 'Memphis Grizzlies'),
        ('MIA', 'Miami Heat'),
        ('MIL', 'Milwaukee Bucks'),
        ('MIN', 'Minnesota Timberwolves'),
        ('NOP', 'New Orleans Pelicans'),
        ('NYK', 'New York Knicks'),
        ('OKC', 'Oklahoma City Thunder'),
        ('ORL', 'Orlando Magic'),
        ('PHI', 'Philadelphia 76ers'),
        ('PHX', 'Phoenix Suns'),
        ('POR', 'Portland Trail Blazers'),
        ('SAC', 'Sacramento Kings'),
        ('SAS', 'San Antonio Spurs'),
        ('TOR', 'Toronto Raptors'),
        ('UTA', 'Utah Jazz'),
        ('WAS', 'Washington Wizards'),
        )
    #home team abv
    home = models.CharField(max_length=3, choices=CHOICES)
    #team color
    homecolor = models.CharField(max_length=10)
    #visitor team abv
    visitor = models.CharField(max_length=3, choices=CHOICES)
    #team html color code
    visitorcolor = models.CharField(max_length=10)

    # game date
    gamedate = models.CharField(max_length=10, default=timezone.now().strftime('%Y-%m-%d'))
    
    #user author of game
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    #time game was created
    date_posted = models.DateTimeField(default=timezone.now)

    #old and not used used to be 0 or 1
    prediction = models.DecimalField(null=True, blank=True, max_digits=4, decimal_places=3)

    #game api id for balldonelie.io
    gameid = models.CharField(null=True, blank=True, max_length=10)

    #actual game scores
    home_score = models.CharField(default='0',null=True, blank=True, max_length=3)
    visitor_score = models.CharField(default='0',null=True, blank=True, max_length=3)

    #game is final and no time left in last period.
    finished = models.BooleanField(default=False)
    
    #point spreads displayed at top and used for predictions
    home_spread = models.CharField(null=True, blank=True, max_length=10)
    visitor_spread = models.CharField(null=True, blank=True, max_length=10)
    dk_home_spread = models.CharField(null=True, blank=True, max_length=10)
    dk_visitor_spread = models.CharField(null=True, blank=True, max_length=10)


    #game winner 0 for visitor 1 for home
    winner = models.IntegerField(null=True, blank=True, default=0)

    #id used to match game instance to csv file
    csvid = models.CharField(null=True, blank=True, max_length=10)

    #predicted scores
    home_score_prediction = models.CharField(null=True, blank=True, max_length=10)
    visitor_score_prediction = models.CharField(null=True, blank=True, max_length=10)

    #pmscore for plus minus score or home predicted score minus visitor predicted score
    pmscore = models.FloatField(null=True, blank=True, default=0)
    
    #team data games won/loss
    home_games_won = models.CharField(null=True, blank=True, max_length=10)
    home_games_loss = models.CharField(null=True, blank=True, max_length=10)
    visitor_games_won = models.CharField(null=True, blank=True, max_length=10)
    visitor_games_loss = models.CharField(null=True, blank=True, max_length=10)

    #streak data
    visitor_streak = models.CharField(null=True, blank=True, max_length=10)
    home_streak = models.CharField(null=True, blank=True, max_length=10)
    
    #margin is greater then x and won
    ev_won = models.CharField(null=True, blank=True, max_length=10)
    ev_margin1 = models.CharField(null=True, blank=True, max_length=10)
    ev_margin2 = models.CharField(null=True, blank=True, max_length=10)
    ev_margin3 = models.CharField(null=True, blank=True, max_length=10)

    #margin abs(pmscore-spread)
    margin = models.CharField(null=True, blank=True, max_length=10)
    #home injury data
    homeInjury = models.CharField(null=True, blank=True, max_length=1000)
    homeInjuryComplex = models.CharField(null=True, blank=True, max_length=10000)
    #visitor injury data
    visitorInjury = models.CharField(null=True, blank=True, max_length=1000)
    visitorInjuryComplex = models.CharField(null=True, blank=True, max_length=10000)
    #dump of player id removed from game
    removed_players = models.CharField(null=True, blank=True, max_length=1000)
    #0 visitor 1 home team predict win with fanduel spread
    spread_prediction = models.CharField(null=True, blank=True, max_length=10)
    
    #t/f marked bet
    bet = models.BooleanField(default=False)
    #int model number 0-2
    model = models.CharField(default='0', max_length=10)
    #dump of complex spread data used in table at bottom of game
    complexSpread = models.CharField(null=True, blank=True, max_length=10000)


    #home last game
    home_last_game = models.CharField(null=True, blank=True, max_length=15)
    home_history = models.CharField(null=True, blank=True, max_length=100000000)
    home_history2 = models.CharField(null=True, blank=True, max_length=100000000)

    #visitor last game
    visitor_last_game = models.CharField(null=True, blank=True, max_length=15)
    visitor_history = models.CharField(null=True, blank=True, max_length=100000000)
    visitor_history2 = models.CharField(null=True, blank=True, max_length=100000000)

    #player Ids
    p0 = models.CharField(null=True, blank=True, max_length=10)
    p1 = models.CharField(null=True, blank=True, max_length=10)
    p2 = models.CharField(null=True, blank=True, max_length=10)
    p3 = models.CharField(null=True, blank=True, max_length=10)
    p4 = models.CharField(null=True, blank=True, max_length=10)
    p5 = models.CharField(null=True, blank=True, max_length=10)
    p6 = models.CharField(null=True, blank=True, max_length=10)
    p7 = models.CharField(null=True, blank=True, max_length=10)
    p8 = models.CharField(null=True, blank=True, max_length=10)
    p9 = models.CharField(null=True, blank=True, max_length=10)
    p10 = models.CharField(null=True, blank=True, max_length=10)
    p11 = models.CharField(null=True, blank=True, max_length=10)
    p12 = models.CharField(null=True, blank=True, max_length=10)
    p13 = models.CharField(null=True, blank=True, max_length=10)
    p14 = models.CharField(null=True, blank=True, max_length=10)
    p15 = models.CharField(null=True, blank=True, max_length=10)
    p16 = models.CharField(null=True, blank=True, max_length=10)
    p17 = models.CharField(null=True, blank=True, max_length=10)        
    p18 = models.CharField(null=True, blank=True, max_length=10)
    simpleRecord = models.BooleanField(default=False)




    def __str__(self):
        return str(self.author)



    def get_absolute_url(self):
        
        return reverse('edit-predict', kwargs={'pk': self.pk})
        











        
class TensorflowModel(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)
    ip = models.CharField(null=True, blank=True, max_length=50)
    model_number = models.CharField(null=True, blank=True, max_length=50)


        
class PermaGame(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)
    ip = models.CharField(null=True, blank=True, max_length=50)



class Retrain(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)
    ip = models.CharField(null=True, blank=True, max_length=50)
    model = models.CharField(null=True, blank=True, max_length=50)
    strength = models.CharField(null=True, blank=True, max_length=50)



class ModelReset(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)
    ip = models.CharField(null=True, blank=True, max_length=50)
    model = models.CharField(null=True, blank=True, max_length=50)



class ArbLoad(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)
    ip = models.CharField(null=True, blank=True, max_length=50)



