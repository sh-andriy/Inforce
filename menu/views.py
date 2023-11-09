from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.utils import timezone
from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from .models import Menu, Vote
from .serializers import MenuSerializer, VoteSerializer, CurrentDayMenuSerializer
from restaurant.models import Restaurant


class MenuCreateView(generics.CreateAPIView):
    """
    View to create a new menu for a restaurant. Only admin users can create a menu.
    """
    permission_classes = [permissions.IsAdminUser]
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

    def perform_create(self, serializer):
        restaurant_id = self.request.data.get('restaurant')
        restaurant = generics.get_object_or_404(Restaurant, pk=restaurant_id)
        serializer.save(restaurant=restaurant)


class CurrentDayMenuListView(generics.ListAPIView):
    """
    View to list the menu for the current day for all restaurants or a specific one if 'restaurant_id' is provided.
    """
    permission_classes = [
        permissions.AllowAny]  # Assuming it's open to all users
    serializer_class = CurrentDayMenuSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned menus to a given restaurant,
        by filtering against a 'restaurant_id' query parameter in the URL.
        """
        queryset = Menu.objects.filter(date=timezone.now().date())
        restaurant_id = self.request.query_params.get('restaurant_id')
        if restaurant_id is not None:
            queryset = queryset.filter(restaurant_id=restaurant_id)
        return queryset


class VoteCreateView(generics.CreateAPIView):
    """
    View for creating a vote for a menu by an employee.
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer

    def perform_create(self, serializer):
        # Get the menu that the vote is for
        menu_id = self.request.data.get('menu')
        menu = generics.get_object_or_404(Menu, pk=menu_id)

        # Ensure the authenticated user has an employee profile
        try:
            employee = self.request.user.employee
        except ObjectDoesNotExist:
            raise ValidationError('No employee profile exists for this user.')

        # Check if the employee has already voted for this menu and date
        vote_exists = Vote.objects.filter(
            employee=employee, menu=menu).exists()
        if vote_exists:
            raise ValidationError('You have already voted for today\'s menu.')

        serializer.save(employee=employee, menu=menu)


class MenuResultsView(generics.RetrieveAPIView):
    """
    View to get the voting results for a specific menu.
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

    def retrieve(self, request, *args, **kwargs):
        menu = self.get_object()
        votes = Vote.objects.filter(menu=menu).count()
        return Response({'menu_id': menu.id, 'votes': votes})


class CurrentDayMenuResultsView(generics.ListAPIView):
    """
    View to get the voting results for all menus on the current day.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MenuSerializer

    def get_queryset(self):
        return Menu.objects.filter(
            date=timezone.now().date()).annotate(
            votes_count=Count('votes')).order_by('-votes_count')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        if queryset:
            max_votes = queryset[0].votes_count
            winning_menus = queryset.filter(votes_count=max_votes)

            serializer = self.get_serializer(winning_menus, many=True)
            return Response({
                'date': timezone.now().date(),
                'winning_menus': serializer.data,
                'max_votes': max_votes,
            })
        else:
            return Response({
                'date': timezone.now().date(),
                'message': 'No menus available for voting today.'
            })
