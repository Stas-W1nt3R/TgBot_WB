from django.contrib import admin
from .models import Cryptocurrency, TgUser, UserTracking

admin.register(Cryptocurrency)
admin.register(TgUser)
admin.register(UserTracking)
