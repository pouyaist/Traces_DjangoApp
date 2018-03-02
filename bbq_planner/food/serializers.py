from rest_framework import serializers
from food.models import FoodOrder, Food


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ('id', 'source', 'food_type')


class FoodOrderSerializer(serializers.ModelSerializer):
    food = FoodSerializer()
    class Meta:
        model = FoodOrder
        fields = ('id', 'number', 'food')
