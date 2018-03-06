from django.contrib import admin

from food.models import Food, FoodOrder

class FoodAdmin(admin.ModelAdmin):
    model = Food
    list_display = ['id', 'source', 'food_type']


class FoodOrderAdmin(admin.ModelAdmin):
    model = FoodOrder
    list_display = ['id', 'food', 'number', 'created_at', 'updated_at']



admin.site.register(Food, FoodAdmin)
admin.site.register(FoodOrder, FoodOrderAdmin)
