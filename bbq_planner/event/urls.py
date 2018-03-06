from django.urls import path, re_path
from event.views import (EventItemResources, EventInstanceResources,
                        EventResources, EventTemplateResources)


urlpatterns = [
    path('', EventResources.as_view(), name='event_list'),
    path('item/create/', EventTemplateResources.as_view(), name='get_event_template'),
    path('item/', EventItemResources.as_view(), name='event_item'),
    re_path('^item/(?P<event_date>.+)/(?P<name>.+)$',
            EventInstanceResources.as_view(), name='event_url'),
]
