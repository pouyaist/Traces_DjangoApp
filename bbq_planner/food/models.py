from django.db import models


class Food(models.Model):
    id = models.AutoField(primary_key=True)
    source = models.CharField(max_length=200, default= "animal")
    food_type = models.CharField(max_length=200, default = "beef", unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'food'

    def save(self, *args, **kwargs):
        self.source = self.source.lower()
        self.food_type = self.food_type.lower()
        super(Food, self).save(*args, **kwargs)


class FoodOrder(models.Model):
    id = models.AutoField(primary_key=True)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    number = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'food_orders'
