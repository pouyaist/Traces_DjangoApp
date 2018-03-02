import factory
from food.models import Food, FoodOrder


class FoodFactory(factory.Factory):
    class Meta:
        model = Food
    source = "Animal"
    food_type = "Pork"



class FoodOrderFactory(factory.Factory):
    class Meta:
        model = FoodOrder
    food= factory.SubFactory(FoodFactory)
    number = 5
