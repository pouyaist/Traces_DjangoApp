from django.urls import path
from user.views import  AttendeeResources, register


urlpatterns = [
    path('register/', register, name='register'),
    path('attend/', AttendeeResources.as_view(), name='attend'),
]
