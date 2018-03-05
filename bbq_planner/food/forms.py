from django import forms
from food.models import Food, FoodOrder


class FoodForm(forms.Form):
    class Meta:
        model = Food
        fields = ['source', 'food_type']


class FoodOrderForm(forms.Form):
    class Meta:
        model = FoodOrder
        fields = ['food', 'number']
