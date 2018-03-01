from django.db import models


class Food(models.Model):
    id = models.AutoField(primary_key=True)
    source = models.CharField(max_length=200, default= "meat")
    food_type = models.CharField(max_length=200, default = "beef")

    class Meta:
        db_table = 'food'


class FoodOrder(models.Model):
    id = models.AutoField(primary_key=True)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    number = models.PositiveIntegerField(default=1)

    class Meta:
        db_table = 'food_orders'
