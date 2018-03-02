import factory
from food.models import Food, FoodOrder


class FoodFactory(factory.Factory):
    class Meta:
        model = Food
    source = "animal"
    food_type = "pork"



class FoodOrderFactory(factory.Factory):
    class Meta:
        model = FoodOrder
    food= factory.SubFactory(FoodFactory)
    number = 5
