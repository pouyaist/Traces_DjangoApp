from django.db import transaction
from django.shortcuts import render
from django.template import loader

from datetime import datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from user.models import Attendee
from user.forms import UserAuthForm, UserExtendForm
from food.models import FoodOrder
from event.models import Event, EventAttendee

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
        loader.get_template('registration/registration.html')
        user_auth_form = UserAuthForm()
        user_extended_form = UserExtendForm()
        return render(request, 'registration/registration.html',
                      {'user_auth_form': user_auth_form, 'user_extended_form': user_extended_form})


class EventAttendeeResources(APIView):
    permission_classes = ()
    authentication_classes = ()

    #TODO check all the APIs edge cases
    #TODO create a cutom error page
    @transaction.atomic
    def post(self, request, event_date, event_name):
        try:
            event_date = datetime.strptime(event_date, "%Y-%m-%d").date()
        except ValueError:
             return Response({'failue': 'event date is not well formated'},
                         status=status.HTTP_400_BAD_REQUEST)

        events = Event.objects.filter(name = event_name,
            event_date = event_date)
        if not events.exists():
            return Response({'reason': f"there is no event with the name:\
                     {event_name} and the date {str(event_date)} "},
                      status=status.HTTP_404_NOT_FOUND)
        #TODO use .create - optimize select_related
        current_event = events[0]

        attendee_first_name = request.data.get('first_name')
        attendee_last_name = request.data.get('last_name')
        number_of_guests = request.data.get('number_of_guests')

        foods  = current_event.food_types.all()
        food_list = {}

        food_types = foods.values_list('food_type', flat=True)

        for key, value in request.data.items():
            if (key  in food_types) and int(value) > 0:
                food_list[key] = int(value)

        if ((attendee_first_name in [[], '', None, {}])
            or (attendee_last_name in [[], '', None, {}])
            or (food_list in [[], '', None, {}])):
            return Response({'failue': 'some of the inputs are empty'},
                        status=status.HTTP_400_BAD_REQUEST)

        food_orders = []

        for food_type, number in food_list.items():
            food_order = FoodOrder(food = foods.get(food_type=food_type),
                                number = number)
            food_order.save()
            food_orders.append(food_order)
        try:
            attendee, _ = Attendee.objects.get_or_create(
                first_name = attendee_first_name,
                last_name = attendee_last_name)
        except ValueError:
            return Response({"reason": "attendee format is wrong"},
                    status=status.HTTP_400_BAD_REQUEST)
        try:
            event_attendee = EventAttendee(event = current_event,
                attendee = attendee, number_of_guests = number_of_guests)
            event_attendee.save()
        except ValueError:
            return Response({"reason": "event_attendee format is wrong"},
                    status=status.HTTP_400_BAD_REQUEST)

        for food_order in food_orders:
            event_attendee.food_orders.add(food_order)

        return Response({'success': " attendee is successfully\
                    registered to the event"}, status=status.HTTP_201_CREATED)
