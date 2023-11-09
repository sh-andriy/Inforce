from django.urls import path
from .views import RestaurantCreateView, RestaurantListView

urlpatterns = [
    path('create/', RestaurantCreateView.as_view(), name='restaurant-create'),
    path('list/', RestaurantListView.as_view(), name='restaurant-list'),
]
