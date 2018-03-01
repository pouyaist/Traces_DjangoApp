from django.urls import path
from user import views


urlpatterns = [
    path('register/', views.register, name='register'),
    #path('attend/', views.attend, name='attend'),
]
