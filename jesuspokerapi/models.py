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

    def get_current_score(self):
        total_score = self.get_total_score()
        f = open("./log.txt", "a")
        f.write(self)
        f.close()
        paid_out = self.payments_paid.aggregate(Sum('amount'))['amount__sum'] or 0
        paid_in = self.payments_received.aggregate(Sum('amount'))['amount__sum'] or 0
        return total_score - paid_in + paid_out

    def __str__(self):
        return self.name


class Session(models.Model):
    date = models.DateField()
    # creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_sessions", null=True )
    players = models.ManyToManyField(Player)
    balance = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    def __str__(self):
        return str(self.date)


class SessionResult(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='sessions')
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='results')
    result = models.DecimalField(max_digits=5, decimal_places=2)


class Payment(models.Model):
    payer = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="payments_paid")
    payee = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="payments_received")
    amount = models.DecimalField(max_digits=5, decimal_places=2)
