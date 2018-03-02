from rest_framework import serializers
from event.models import Event, EventAttendee
from user.serializers import AttendeeSerializer
from food.serializers import FoodOrderSerializer

class EventSerializer(serializers.ModelSerializer):
    organizer_name = serializers.SerializerMethodField()
    number_of_attendees = serializers.SerializerMethodField()
    list_of_attendees = serializers.SerializerMethodField()
    food_order_number_list = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ('id', 'name', 'organizer_name', 'category',
         'list_of_attendees', 'number_of_attendees', 'event_date',
         'food_order_number_list', 'url')

    def get_organizer_name(self, obj):
        return obj.organizer.user_auth.get_full_name()

    def get_number_of_attendees(self, obj):
        numbet_of_participants = 0
        for eventattendee in obj.eventattendee_set.all():
            numbet_of_participants += \
             (eventattendee.number_of_guests + 1)
        return numbet_of_participants

    def get_list_of_attendees(self, obj):
        attendees_names = []
        for eventattendee in obj.eventattendee_set.all():
             attendees_names.append(eventattendee.attendee.get_full_name())
        return attendees_names

    def get_food_order_number_list(self, obj):
        food_order_number_list = {}
        for eventattendee in obj.eventattendee_set.all():
            for food_order in eventattendee.food_orders.all():
                if food_order.food.food_type in food_order_number_list:
                    food_order_number_list[food_order.food.food_type ] += food_order.number
                else:
                    food_order_number_list[food_order.food.food_type ] = food_order.number
        return food_order_number_list


class EventAttendeeSerializer(serializers.ModelSerializer):
    event = EventSerializer()
    attendee = AttendeeSerializer()
    food_orders = FoodOrderSerializer(many = True)

    class Meta:
        model = EventAttendee
        fields = ('event', 'attendee', 'number_of_guests', 'food_orders')
