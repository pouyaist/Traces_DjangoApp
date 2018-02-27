from django.urls import path, include
from home import views

urlpatterns = [
    path('', views.index, name='index'),
    #url(r'^oauth/', include('social_django.urls', namespace='social')),
]
