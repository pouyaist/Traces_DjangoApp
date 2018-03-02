from django.urls import path, re_path
from user.views import  AttendeeResources, register


urlpatterns = [
    path('register/', register, name='register'),
    re_path('^attend/(?P<event_date>.+)/(?P<event_name>.+)$',
                AttendeeResources.as_view(), name='attend'),
]
