from rest_framework import serializers
from .models import Menu, Dish, Vote


class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = ['id', 'name', 'description']


class MenuSerializer(serializers.ModelSerializer):
    dishes = DishSerializer(many=True, required=False)

    class Meta:
        model = Menu
        fields = ['id', 'restaurant', 'date', 'name', 'description', 'dishes']

    def create(self, validated_data):
        dishes_data = validated_data.pop('dishes', [])
        menu = Menu.objects.create(**validated_data)
        for dish_data in dishes_data:
            Dish.objects.create(menu=menu, **dish_data)
        return menu

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.save()
        return instance


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ('id', 'menu', 'employee', 'created_at')
        read_only_fields = ('employee',)


class CurrentDayMenuSerializer(serializers.ModelSerializer):
    dishes = DishSerializer(many=True)

    class Meta:
        model = Menu
        fields = ['id', 'restaurant', 'date', 'name', 'description', 'dishes']
