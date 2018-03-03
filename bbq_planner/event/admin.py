from django.contrib import admin

from event.models import Event

class EventAdmin(admin.ModelAdmin):
    model = Event

admin.site.register(Event, EventAdmin)
