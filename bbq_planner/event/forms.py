from django import forms
from event.models import Event, EventAttendee

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'event_date', 'category', 'event_date', 'food_types']


class EventAttendeeForm(forms.ModelForm):
    class Meta:
        model = EventAttendee
        fields = ['event', 'attendee', 'number_of_guests', 'food_orders']


def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['password'].widget.attrs['class'] = 'form-control'
