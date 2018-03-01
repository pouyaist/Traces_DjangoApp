from django.urls import path
from event.views import EventItemResources, EventResources


urlpatterns = [
    path('', EventResources.as_view(), name='events'),
    path('item/', EventItemResources.as_view(), name='event_item'),
]
