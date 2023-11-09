from django.contrib import admin
from .models import Menu, Dish, Vote


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ['restaurant', 'date', 'name']
    list_filter = ['restaurant', 'date']
    search_fields = ['name', 'restaurant__name']
    date_hierarchy = 'date'


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ['name', 'menu', 'description']
    list_filter = ['menu']
    search_fields = ['name', 'menu__name']


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ['menu', 'employee', 'created_at']
    list_filter = ['menu', 'employee']
    search_fields = ['menu__name', 'employee__user__email']
