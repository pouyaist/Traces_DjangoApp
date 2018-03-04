from django.contrib import admin

from food.models import Food, FoodOrder

class FoodAdmin(admin.ModelAdmin):
    model = Food


class FoodOrderAdmin(admin.ModelAdmin):
    model = FoodOrder



admin.site.register(Food, FoodAdmin)
admin.site.register(FoodOrder, FoodOrderAdmin)
