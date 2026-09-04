from django.contrib import admin
from .models import Cryptocurrency, TgUser, UserTracking

admin.site.register(Cryptocurrency)
admin.site.register(TgUser)
admin.site.register(UserTracking)
