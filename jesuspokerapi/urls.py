from django.urls import path,include
from . import views
from rest_framework import routers

rtr = routers.DefaultRouter()
rtr.register('players', views.PlayerView)
rtr.register('sessions', views.SessionView)
rtr.register('sessionsresults', views.SessionResultView)

urlpatterns = [
    path('', include(rtr.urls))
]