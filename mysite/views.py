from urllib import request

from .models import Product, TgUser, UserTracking
from rest_framework import viewsets
from .serializers import ProductSerializer, TgUserSerializer, UserTrackingSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class TgUserViewSet(viewsets.ModelViewSet):
    queryset = TgUser.objects.filter(user=request.user)
    serializer_class = TgUserSerializer


class UserTrackingViewSet(viewsets.ModelViewSet):
    queryset = UserTracking.objects.all()
    serializer_class = UserTrackingSerializer
