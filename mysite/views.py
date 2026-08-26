from urllib import request
from .models import Cryptocurrency, TgUser, UserTracking
from rest_framework import viewsets
from .serializers import CryptocurrencySerializer, TgUserSerializer, UserTrackingSerializer


class CryptocurrencyViewSet(viewsets.ModelViewSet):
    queryset = Cryptocurrency.objects.all()
    serializer_class = CryptocurrencySerializer


class TgUserViewSet(viewsets.ModelViewSet):
    queryset = TgUser.objects.all()
    serializer_class = TgUserSerializer

    def get_queryset(self):
        queryset = TgUser.objects.filter(user=self.request.user)


class UserTrackingViewSet(viewsets.ModelViewSet):
    queryset = UserTracking.objects.all()
    serializer_class = UserTrackingSerializer
