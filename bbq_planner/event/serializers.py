from rest_framework import serializers
from event.models import Event

#TODO add the number of guests per attendee
class EventSerializer(serializers.ModelSerializer):
    organizer_name = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ('id', 'name', 'organizer_name', 'category',
         'event_date', 'url')

    def get_organizer_name(self, obj):
        return obj.organizer.user_auth.get_full_name()
