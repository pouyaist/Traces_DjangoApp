from django.db import models
from user.models import UserProfile, Attendee
from food.models import FoodOrder, Food


class Event(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank = True)
    organizer = models.ForeignKey(UserProfile,
        on_delete=models.SET_NULL, null=True)
    attendees = models.ManyToManyField(Attendee, through='EventAttendee')
    category = models.CharField(max_length=50, default = "BBQ")
    food_types = models.ManyToManyField(Food)
    event_date = models.DateField()
    url = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'events'
        unique_together = ("name", "event_date")


class EventAttendee(models.Model):
    id = models.AutoField(primary_key=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    attendee = models.ForeignKey(Attendee, on_delete=models.CASCADE)
    number_of_guests = models.IntegerField(default=0)
    food_orders = models.ManyToManyField(FoodOrder)

    class Meta:
        db_table = 'event_attendees'
