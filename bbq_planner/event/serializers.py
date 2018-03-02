from rest_framework import serializers
from event.models import Event

#TODO add the number of guests per attendee
class EventSerializer(serializers.ModelSerializer):
    organizer_name = serializers.SerializerMethodField()
    number_of_attendees = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ('id', 'name', 'organizer_name', 'category',
        'number_of_attendees', 'event_date', 'url')

    def get_organizer_name(self, obj):
        return obj.organizer.user_auth.get_full_name()

    def get_number_of_attendees(self, obj):
        return len(obj.attendees.all())
