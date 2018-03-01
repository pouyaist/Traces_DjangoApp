from django.shortcuts import render
from django.contrib.auth.models import User as AuthUser
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.db import IntegrityError, transaction

from datetime import datetime, date, timedelta

from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import permissions, status, authentication

from event.models import Event

class EventResources(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @transaction.atomic
    def post(self, request):
        user = request.user
        event_name = request.data.get('name')
        category = request.data.get('category')
        string_event_date = request.data.get('event_date')
        event_date = datetime.strptime(string_event_date, "%Y-%m-%d").date()
        if event_date < date.today():
            return Response({'failue': " event date is for the past"},
                        status=status.HTTP_400_BAD_REQUEST)

        if Event.objects.filter(name = event_name, category = category,
         event_date = event_date, organizer = user.userprofile).exists():
            return Response({'failue': " event is already created"},
                        status=status.HTTP_400_BAD_REQUEST)

        Event(name = event_name, category = category,
         event_date = event_date, organizer = user.userprofile).save()
        return Response({'success': " event is successfully created"},
                        status=status.HTTP_201_CREATED)
