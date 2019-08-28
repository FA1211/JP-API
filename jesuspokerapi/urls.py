from django.urls import path,include
from . import views
from rest_framework import routers

rtr = routers.DefaultRouter()
rtr.register('players', views.PlayerView)
rtr.register('forms', views.FormView)
rtr.register('sessions',views.SessionView)
rtr.register('sessionsresults', views.SessionResultView)
rtr.register('playerscores',views.PlayerScoreView)


urlpatterns = [
    path('', include(rtr.urls))
]