from django.urls import path,include
from jesuspokerapi.views import views
from rest_framework import routers

from jesuspokerapi.views.LoginVerifyView import LoginVerifyView
from jesuspokerapi.views.SocialLoginView import SocialLoginView

rtr = routers.DefaultRouter()
rtr.register('api/players', views.PlayerView)
rtr.register('api/forms', views.FormView)
rtr.register('api/sessions', views.SessionView)
rtr.register('api/sessionsresults', views.SessionResultView)
rtr.register('api/playerscores', views.PlayerScoreView)

urlpatterns = [
    path('', include(rtr.urls)),
    path('api/auth/login/', SocialLoginView.as_view()),
    path('api/auth/oauth/', include('rest_framework_social_oauth2.urls')),
    path('api/auth/check-token/', LoginVerifyView.as_view())
]