from rest_framework import serializers
from user.models import Attendee
from food.serializers import FoodOrderSerializer


class AttendeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attendee
        fields = ('id', 'first_name', 'last_name')
