from django.contrib import admin
from .models import Cryptocurrency, TgUser, UserTracking


@admin.register(Cryptocurrency)
class CryptocurrencyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'coin_id', 'price')
    search_fields = ('name','coin_id')
    list_filter = ('name',)

@admin.register(TgUser)
class TgUserAdmin(admin.ModelAdmin):
    list_display = ('id','telegram_id' , 'username')
    search_fields = ('telegram_id', 'username')

@admin.register(UserTracking)
class UserTrackingAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'cryptocurrency','target_price', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('user__username', 'cryptocurrency__name')
