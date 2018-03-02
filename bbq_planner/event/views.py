from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from datetime import datetime, date, timedelta
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import permissions, status, authentication
from event.models import Event
from event.serializers import EventSerializer
from user.models import UserProfile



class EventItemResources(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    #TODO update URL
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

        #TODO update static url
        url = "http://localhost:8000" + f"/item/{string_event_date}/{event_name}"
        event = Event(name = event_name, category = category, url = url,
                event_date = event_date, organizer = user.userprofile)
        event.save()
        return Response({'success':
                        f" event {event.id} is successfully created"},
                        status=status.HTTP_201_CREATED)


class EventResources(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        if request.user.is_staff:
            return HttpResponseRedirect(redirect_to="/admin/")
        if request.user.userprofile is None:
            return Response(events.data, status=status.HTTP_404_NOT_FOUND)
        events = Event.objects.filter(organizer_id = request.user.userprofile.id)

        if not events:
            return Response([], status=status.HTTP_200_OK)
        events = EventSerializer(events, many=True)
        return Response(events.data, status=status.HTTP_200_OK)


class EventInstanceResources(APIView):
    permission_classes = ()
    authentication_classes = ()

    def get(self, request, event_date, name):
        user = request.user
        event_date = datetime.strptime(event_date, "%Y-%m-%d").date()
        events = Event.objects.filter(name = name, event_date = event_date)
        if not events:
            return Response({'reason': f"there is no event with the name:\
                     {name} and the date {str(event_date)} "},
                      status=status.HTTP_404_NOT_FOUND)

        event = EventSerializer(events[0])
        return Response(event.data, status=status.HTTP_200_OK)
