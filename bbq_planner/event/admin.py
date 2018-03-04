from django.contrib import admin

from event.models import Event

#TODO autogenrate url
class EventAdmin(admin.ModelAdmin):
    model = Event

admin.site.register(Event, EventAdmin)
