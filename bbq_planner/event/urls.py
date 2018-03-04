from django.urls import path, re_path
from event.views import (EventItemResources, EventInstanceResources,
                        EventResources)

#TODO optimize urls and resources
urlpatterns = [
    path('', EventResources.as_view(), name='event_list'),
    path('item/', EventItemResources.as_view(), name='event_item'),
    re_path('^item/(?P<event_date>.+)/(?P<name>.+)$',
            EventInstanceResources.as_view(), name='event_url'),
]
