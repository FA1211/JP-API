from django.db import models


# Create your models here.
class Player(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Session(models.Model):
    date = models.DateField()
    balance = models.IntegerField(default=0)

    def __str__(self):
        return str(self.date)


class SessionResult(models.Model):
    player = models.OneToOneField(Player, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='results')
    result = models.IntegerField(default=0)
