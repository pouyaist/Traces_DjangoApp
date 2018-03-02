from django.db import transaction
from django.shortcuts import render
from django.contrib.auth.models import User as AuthUser
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect

from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import permissions, status, authentication
from user.models import Attendee
from user.serializers import AttendeeSerializer
from user.forms import UserAuthForm, UserExtendForm
from food.models import Food, FoodOrder


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
    def post(self, request):
        #TODO exception handling:
        serializer = AttendeeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"reason": serializer.errors},
                    status=status.HTTP_412_PRECONDITION_FAILED)

        attendee_serialized = serializer.data


        food_orders = []
        if not attendee_serialized['food_orders']:
            return Response({"reason": "empty food orders"},
                    status=status.HTTP_412_PRECONDITION_FAILED)
        for food_order in attendee_serialized['food_orders']:
            number = food_order['number']
            if not food_order['food']:
                return Response({"reason": "empty food item"},
                        status=status.HTTP_412_PRECONDITION_FAILED)
            food_source = food_order['food']['source']
            food_type = food_order['food']['food_type']
            food = Food(source = food_source, food_type = food_type)
            food.save()
            food_order = FoodOrder(food = food, number = number)
            food_order.save()
            food_orders.append(food_order)

        attendee = Attendee(first_name = attendee_serialized['first_name'],
            last_name = attendee_serialized['last_name'],
            number_of_guests = attendee_serialized['number_of_guests'])
        attendee.save()
        return Response({'success': " attendee is successfully\
                    registered to the event"}, status=status.HTTP_201_CREATED)
