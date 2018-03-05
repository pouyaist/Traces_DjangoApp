from django.contrib import admin

from event.models import Event


class EventAdmin(admin.ModelAdmin):
    model = Event
    list_display = ('id', 'name', 'organizer_name',
                    'category', 'event_date','url')

    def organizer_name(self, obj):
        return obj.organizer.user_auth.get_full_name()

admin.site.register(Event, EventAdmin)
