from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import Restaurant
from .serializers import RestaurantSerializer


class RestaurantCreateView(generics.CreateAPIView):
    """
    View to create a new restaurant.
    """
    permission_classes = [permissions.IsAdminUser]
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer


class RestaurantListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
