from bbq_planner import settings
from django.urls import path, re_path
from django.views.generic.base import TemplateView
from event.views import (EventItemResources, EventInstanceResources,
                        EventResources, EventTemplateResources)

# Static stuff only for development, aka DEBUG=False
if settings.DEBUG:
    urlpatterns = [
        # Error pages
        re_path('^404/$', TemplateView.as_view(template_name='404.html')),
        re_path(r'^500/$', TemplateView.as_view(template_name='500.html')),
        re_path(r'^400/$', TemplateView.as_view(template_name='400.html')),
    ] + urlpatterns


urlpatterns = [
    path('', EventResources.as_view(), name='event_list'),
    path('item/create/', EventTemplateResources.as_view(), name='get_event_template'),
    path('item/', EventItemResources.as_view(), name='event_item'),
    re_path('^item/(?P<event_date>.+)/(?P<name>.+)$',
            EventInstanceResources.as_view(), name='event_url'),
]
