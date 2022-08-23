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
        ('ATL',	'Atlanta Hawks'),
        ('BKN',	'Brooklyn Nets'),
        ('BOS',	'Boston Cel tics'),
        ('CHA',	'Charlotte Hornets'),
        ('CHI',	'Chicago Bulls'),
        ('CLE',	'Cleveland Cavaliers'),
        ('DAL',	'Dallas Mavericks'),
        ('DEN',	'Denver Nuggets'),
        ('DET',	'Detroit Pistons'),
        ('GSW',	'Golden State Warriors'),
        ('HOU',	'Houston Rockets'),
        ('IND',	'Indiana Pacers'),
        ('LAC',	'Los Angeles Clippers'),
        ('LAL',	'Los Angeles Lakers'),
        ('MEM',	'Memphis Grizzlies'),
        ('MIA',	'Miami Heat'),
        ('MIL',	'Milwaukee Bucks'),
        ('MIN',	'Minnesota Timberwolves'),
        ('NOP',	'New Orleans Pelicans'),
        ('NYK',	'New York Knicks'),
        ('OKC',	'Oklahoma City Thunder'),
        ('ORL',	'Orlando Magic'),
        ('PHI',	'Philadelphia 76ers'),
        ('PHX',	'Phoenix Suns'),
        ('POR',	'Portland Trail Blazers'),
        ('SAC',	'Sacramento Kings'),
        ('SAS',	'San Antonio Spurs'),
        ('TOR',	'Toronto Raptors'),
        ('UTA',	'Utah Jazz'),
        ('WAS',	'Washington Wizards'),
        )
    home = models.CharField(max_length=3, choices=CHOICES)
    visitor = models.CharField(max_length=3, choices=CHOICES)
    gamedate = models.CharField(max_length=10, default=timezone.now().strftime('%Y-%m-%d'))
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)
    prediction = models.DecimalField(null=True, blank=True, max_digits=4, decimal_places=3)
    gameid = models.CharField(null=True, blank=True, max_length=10)
    home_score = models.CharField(null=True, blank=True, max_length=3)
    visitor_score = models.CharField(null=True, blank=True, max_length=3)
    finished = models.BooleanField(default=False)
    home_spread = models.CharField(null=True, blank=True, max_length=10)
    visitor_spread = models.CharField(null=True, blank=True, max_length=10)
    winner = models.IntegerField(null=True, blank=True, default=0)
    csvid = models.CharField(null=True, blank=True, max_length=10)
    p0 = models.CharField(null=True, blank=True, max_length=10)
    p1 = models.CharField(null=True, blank=True, max_length=10)
    p2 = models.CharField(null=True, blank=True, max_length=10)
    p3 = models.CharField(null=True, blank=True, max_length=10)
    p4 = models.CharField(null=True, blank=True, max_length=10)
    p5 = models.CharField(null=True, blank=True, max_length=10)
    def __str__(self):
        return str(self.author)

    def get_absolute_url(self):
        print('asdff----------',self.csvid)
        #return reverse('edit-predict', args={'csvid': self.csvid,'change':'c'})
        return reverse('edit-predict', kwargs={'pk': self.pk})
        #return reverse('edit-predict')
