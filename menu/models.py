from django.db import models
from restaurant.models import Restaurant
from employee.models import Employee
import datetime


class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name='menus', on_delete=models.CASCADE)
    date = models.DateField(default=datetime.date.today)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('restaurant', 'date')  # A restaurant can only have one menu per day

    def __str__(self):
        return f"{self.restaurant.name} Menu for {self.date}"


class Dish(models.Model):
    menu = models.ForeignKey(Menu, related_name='dishes', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


class Vote(models.Model):
    menu = models.ForeignKey(Menu, related_name='votes', on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, related_name='votes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('menu', 'employee')  # An employee can only vote once for each menu

    def __str__(self):
        return f"{self.employee.user.username} voted for {self.menu}"
