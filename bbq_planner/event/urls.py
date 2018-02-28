from django.urls import path
from event.views import EventResources

urlpatterns = [
    path('create/', EventResources.as_view(), name='create'),
]
