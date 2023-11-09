from django.urls import path
from .views import MenuCreateView, CurrentDayMenuListView, VoteCreateView, MenuResultsView, CurrentDayMenuResultsView

urlpatterns = [
    path('create/', MenuCreateView.as_view(), name='menu-create'),
    path('list/', CurrentDayMenuListView.as_view(), name='current-day-menu-list'),
    path('vote/', VoteCreateView.as_view(), name='menu-vote'),
    path('results/<int:pk>/', MenuResultsView.as_view(), name='menu-results'),
    path('results/today/', CurrentDayMenuResultsView.as_view(), name='current-day-menu-results'),

]
