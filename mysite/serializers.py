from rest_framework import serializers
from .models import Product, TgUser, UserTracking


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class TgUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TgUser
        fields = ['telegram_id','username']


class UserTrackingSerializer(serializers.ModelSerializer):
    user = TgUserSerializer(read_only=True)
    product = ProductSerializer(read_only=True)

    class Meta:
        model = UserTracking
        fields = ['user', 'product','target_price']
