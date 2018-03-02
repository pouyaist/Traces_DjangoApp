from rest_framework import serializers
from user.models import Attendee
from food.serializers import FoodOrderSerializer


class AttendeeSerializer(serializers.ModelSerializer):
    food_orders = FoodOrderSerializer(many=True)

    class Meta:
        model = Attendee
        fields = ('id', 'first_name', 'last_name', 'number_of_guests',
         'food_orders')
