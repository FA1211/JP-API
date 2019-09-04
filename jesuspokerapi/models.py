from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum


# Create your models here.
class Player(models.Model):
    name = models.CharField(max_length=10)

    def get_total_score(self):
        sessions = self.sessions
        total_score = sessions.aggregate(Sum('result'))['result__sum']
        return total_score

    def __str__(self):
        return self.name


class Session(models.Model):
    date = models.DateField()
    #creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_sessions", null=True )
    players = models.ManyToManyField(Player)
    balance = models.DecimalField(max_digits=5,decimal_places=2, default=0)

    def __str__(self):
        return str(self.date)


class SessionResult(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='sessions')
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='results')
    result = models.DecimalField(max_digits=5,decimal_places=2)
