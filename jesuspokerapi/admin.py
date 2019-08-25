from django.contrib import admin
from .models import Player, Session, SessionResult

# Register your models here.
admin.site.register(Player)
admin.site.register(Session)
admin.site.register(SessionResult)