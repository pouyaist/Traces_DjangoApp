from django.urls import path, re_path
from user.views import  EventAttendeeResources, register
from django.contrib.auth import views as auth_views


urlpatterns = [
    re_path('^login/$', auth_views.login, name='login'),
    re_path('^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    path('register/', register, name='register'),
    re_path('^attend/(?P<event_date>.+)/(?P<event_name>.+)$',
                EventAttendeeResources.as_view(), name='attend'),
]
