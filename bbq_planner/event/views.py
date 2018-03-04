from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from datetime import datetime, date, timedelta
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework import permissions, status, authentication
from event.models import Event
from event.serializers import EventSerializer, CreateEventSerializer
from user.models import UserProfile
from food.serializers import FoodSerializer



class EventItemResources(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    renderer_classes = [JSONRenderer]
    template_name = 'events/create_event.html'

    @transaction.atomic
    #TODO validate input
    def post(self, request):
        user = request.user
        event_name = request.data.get('name')
        category = request.data.get('category')
        string_event_date = request.data.get('event_date')
        if (event_name or category or string_event_date) in ['', None]:
            return Response({'failue': 'event date is for the past'},
                        status=status.HTTP_400_BAD_REQUEST)
        try:
            event_date = datetime.strptime(string_event_date, "%Y-%m-%d").date()
        except ValueError:
             return Response({'failue': 'event date is not well formated'},
                         status=status.HTTP_400_BAD_REQUEST)
        if event_date < date.today():
            return Response({'failue': 'event date is for the past'},
                        status=status.HTTP_400_BAD_REQUEST)

        if Event.objects.filter(name = event_name, category = category,
         event_date = event_date, organizer = user.userprofile).exists():
            return Response({'failue': 'event is already created'},
                        status=status.HTTP_400_BAD_REQUEST)

        #TODO update static url
        url = "http://localhost:8000" + f"/item/{string_event_date}/{event_name}"
        event = Event(name = event_name, category = category, url = url,
                event_date = event_date, organizer = user.userprofile)
        event.save()
        return Response({'success':
                        f" event {event.id} is successfully created"},
                        status=status.HTTP_201_CREATED)

    def get(self, request):
        event_serializer = CreateEventSerializer()
        #TODO a but in django rest framework
        return Response({'event_serializer': event_serializer},
          status=status.HTTP_200_OK)

class EventResources(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'events/index.html'

    def get(self, request):
        if request.user.userprofile is None:
            return Response({'events': 'there is no userprofile'}, status=status.HTTP_404_NOT_FOUND)
        events = Event.objects.filter(organizer_id = request.user.userprofile.id)

        if not events:
            return Response({'events': 'No Events are in the database'}, status=status.HTTP_200_OK)
        events = EventSerializer(events, many=True)
        return Response({'events': events.data},  status=status.HTTP_200_OK)


class EventInstanceResources(APIView):
    permission_classes = ()
    authentication_classes = ()

    def get(self, request, event_date, name):
        event_date = datetime.strptime(event_date, "%Y-%m-%d").date()
        events = Event.objects.filter(name = name, event_date = event_date)
        if not events:
            return Response({'reason': "there is no event with the name:"\
                     f"{name} and the date {str(event_date)} "},
                      status=status.HTTP_404_NOT_FOUND)

        event = EventSerializer(events[0])
        return Response(event.data, status=status.HTTP_200_OK)
