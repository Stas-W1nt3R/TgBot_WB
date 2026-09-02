from rest_framework import serializers
from .models import Cryptocurrency, TgUser, UserTracking


class CryptocurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Cryptocurrency
        fields = '__all__'


class TgUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TgUser
        fields = ['telegram_id','username']


class UserTrackingSerializer(serializers.ModelSerializer):
    user = TgUserSerializer(read_only=True)
    cryptocurrency = CryptocurrencySerializer(read_only=True)

    class Meta:
        model = UserTracking
        fields = ['user', 'cryptocurrency','target_price','is_active']
