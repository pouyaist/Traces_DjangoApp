"""bbq_planner URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic.base import TemplateView
from bbq_planner import settings

urlpatterns = [
    path('', include('home.urls')),
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('events/', include('event.urls'))
]

# Static stuff only for development, aka DEBUG=False
if settings.DEBUG:
    urlpatterns = [
        # Error pages
        re_path('^404/$', TemplateView.as_view(template_name='404.html')),
        re_path('^500/$', TemplateView.as_view(template_name='500.html')),
        re_path('^400/$', TemplateView.as_view(template_name='400.html')),
    ] + urlpatterns
