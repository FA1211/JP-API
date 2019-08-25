from django.shortcuts import render
from rest_framework import viewsets
from .models import Player, Session, SessionResult
from .serializers import PlayerSerializer, SessionSerializer, SessionResultSerializer


# Create your views here.

class PlayerView(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


class SessionView(viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer


class SessionResultView(viewsets.ModelViewSet):
    queryset = SessionResult.objects.all()
    serializer_class = SessionResultSerializer
