from django.db import models

class Event(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank = True)
    category = models.CharField(max_length=50, default = "BBQ")
    event_date = models.DateField()
    url = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = 'events'
