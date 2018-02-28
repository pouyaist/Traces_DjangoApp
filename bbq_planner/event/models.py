from django.db import models
from user.models import UserProfile, Attendee

class Event(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank = True)
    organizer = models.ForeignKey(UserProfile,
        on_delete=models.SET_NULL, null=True)
    attendees = models.ManyToManyField(Attendee, blank=True)
    category = models.CharField(max_length=50, default = "BBQ")
    event_date = models.DateField()
    url = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = 'events'
