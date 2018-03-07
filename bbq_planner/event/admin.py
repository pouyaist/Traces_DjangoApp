from django.contrib import admin

from event.models import Event


class EventAdmin(admin.ModelAdmin):
    model = Event
    list_display = ('id', 'name', 'organizer',
                    'category', 'event_date','url')


admin.site.register(Event, EventAdmin)
