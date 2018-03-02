from django.db import transaction
from django.shortcuts import render
from django.contrib.auth.models import User as AuthUser
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect

from datetime import datetime, date, timedelta

from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import permissions, status, authentication
from user.models import Attendee
from user.serializers import AttendeeSerializer
from user.forms import UserAuthForm, UserExtendForm
from food.models import Food, FoodOrder
from event.models import Event, EventAttendee
from event.serializers import EventAttendeeSerializer


def register(request):
    if request.method == 'POST':
        user_auth_form = UserAuthForm(request.POST)
        user_extended_form = UserExtendForm(request.POST)
        if user_auth_form.is_valid() and user_extended_form.is_valid():
            user = user_auth_form.save(commit=False)
            user.set_password(user.password)
            user.save()
            user.refresh_from_db()
            user_extended = user_extended_form.save(commit=False)
            user_extended.user_auth = user
            user_extended.save()
            return render(request, 'registration/login.html', {'form': user_auth_form}, status=200)
        return render(request, 'registration/registration.html', {'error_form': user_auth_form}, status=400)

    elif request.method == 'GET':
        template = loader.get_template('registration/registration.html')
        user_auth_form = UserAuthForm()
        user_extended_form = UserExtendForm()
        return render(request, 'registration/registration.html',
                      {'user_auth_form': user_auth_form, 'user_extended_form': user_extended_form})


class AttendeeResources(APIView):
    permission_classes = ()
    authentication_classes = ()

    @transaction.atomic
    def post(self, request, event_date, event_name):
        event_date = datetime.strptime(event_date, "%Y-%m-%d").date()
        events = Event.objects.filter(name = event_name,
            event_date = event_date)
        if not events.exists():
            return Response({'reason': f"there is no event with the name:\
                     {event_name} and the date {str(event_date)} "},
                      status=status.HTTP_404_NOT_FOUND)
        current_event = events[0]
        event_attendee_serialized = request.data

        food_orders = []
        if not event_attendee_serialized['food_orders']:
            return Response({"reason": "empty food orders"},
                    status=status.HTTP_412_PRECONDITION_FAILED)
        for food_order in event_attendee_serialized['food_orders']:
            number = food_order['number']
            if not food_order['food']:
                return Response({"reason": "empty food item"},
                        status=status.HTTP_412_PRECONDITION_FAILED)
            food_source = food_order['food']['source']
            food_type = food_order['food']['food_type']
            try:
                food, _ = Food.objects.get_or_create(source = food_source,
                                          food_type = food_type)
            except ValueError:
                return Response({"reason": "food format is wrong"},
                        status=status.HTTP_412_PRECONDITION_FAILED)

            food_order = FoodOrder(food = food, number = number)
            food_order.save()
            food_orders.append(food_order)
        try:
            attendee, _ = Attendee.objects.get_or_create(
                first_name = event_attendee_serialized['attendee']['first_name'],
                last_name = event_attendee_serialized['attendee']['last_name'])
        except ValueError:
            return Response({"reason": "attendee format is wrong"},
                    status=status.HTTP_412_PRECONDITION_FAILED)
        try:
            event_attendee = EventAttendee(event = current_event,
                attendee = attendee,
                number_of_guests = event_attendee_serialized['number_of_guests'])
            event_attendee.save()
        except ValueError:
            return Response({"reason": "event_attendee format is wrong"},
                    status=status.HTTP_412_PRECONDITION_FAILED)

        #TODO is there anyway to do it better
        for food_order in food_orders:
            event_attendee.food_orders.add(food_order)

        return Response({'success': " attendee is successfully\
                    registered to the event"}, status=status.HTTP_201_CREATED)
