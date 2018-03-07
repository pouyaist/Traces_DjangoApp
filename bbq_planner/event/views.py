from django.db import transaction
from django.conf import settings
from django.shortcuts import redirect
from datetime import date, datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework import permissions, status
from rest_framework.decorators import (api_view,
                            permission_classes, renderer_classes)
from event.models import Event
from event.serializers import EventSerializer, CreateEventSerializer
from event.forms import EventForm
from food.models import Food

class EventTemplateResources(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'events/create_event.html'

    def get(self, request):
        event_form = EventForm()
        food_types = Food.objects.all().values_list('food_type', flat = True)
        #TODO change this
        return Response({'event_form': event_form, 'food_types': food_types},
          template_name = 'events/create_event.html', status=status.HTTP_200_OK)


class EventItemResources(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    renderer_classes = [JSONRenderer]
    template_name = 'events/create_event.html'

    @transaction.atomic
    def post(self, request):
        user = request.user

        event_name = request.data.get('name')
        category = request.data.get('category')
        food_types = []
        for food_type, food_type_boolean in request.data.items():
            if food_type_boolean == 'on':
                food_types.append(food_type)

        string_event_date = request.data.get('event_date')
        if ((event_name  in [[], '', None]) or
            (category  in [[], '', None] ) or
            (string_event_date in ['', None])or
            (food_types == [])):
            return Response({'failue': 'some of the inputs are empty'},
                        status=status.HTTP_400_BAD_REQUEST)
        try:
            event_date = datetime.strptime(string_event_date, "%Y-%m-%d").date()
        except ValueError:
             return Response({'failue': 'event date is not well formated'},
                         status=status.HTTP_400_BAD_REQUEST)
        if event_date < date.today():
            return Response({'failue': 'event date is for the past'},
                        status=status.HTTP_400_BAD_REQUEST)

        if Event.objects.filter(name = event_name,
                                event_date = event_date).exists():
            return Response({'failue': 'event is already created'},
                        status=status.HTTP_400_BAD_REQUEST)
        #use cache for object fetching
        foods = Food.objects.all()
        food_types_list = foods.values_list('food_type', flat = True)
        for food_type in food_types:
            if food_type not in food_types_list:
                return Response({'failue':
                            f"food id {food_type} is not correct"},
                            status=status.HTTP_400_BAD_REQUEST)
        event_name_url = '%20'.join(event_name.split(' '))
        url = settings.ROOT_URL + f"/events/item/{string_event_date}/{event_name_url}"
        event = Event(name = event_name, category = category, url = url,
                event_date = event_date, organizer = user.userprofile)
        event.save()
        for food_type in food_types:
            event.food_types.add(foods.get(food_type = food_type))
        return redirect('/events/')


class EventResources(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'events/index.html'

    def get(self, request):
        if request.user.userprofile is None:
            return Response({'events': 'there is no userprofile'},
                            status=status.HTTP_404_NOT_FOUND)
        events = Event.objects.filter(organizer_id = request.user.userprofile.id)
        if not events:
            return Response({'events': 'No Events are in the database'},
                            status=status.HTTP_200_OK)
        events = EventSerializer(events, many=True)
        return Response({'events': events.data},  status=status.HTTP_200_OK)


class EventInstanceResources(APIView):
    permission_classes = ()
    authentication_classes = ()
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'events/event_item.html'

    def get(self, request, event_date, name):
        event_date = datetime.strptime(event_date, "%Y-%m-%d").date()
        events = Event.objects.filter(name = name, event_date = event_date)
        if not events:
            return Response({'reason': "there is no event with the name:"\
                     f"{name} and the date {str(event_date)} "},
                      status=status.HTTP_404_NOT_FOUND)

        event_serializer = EventSerializer(events[0])
        return Response({'event': event_serializer.data},
                        status=status.HTTP_200_OK)
