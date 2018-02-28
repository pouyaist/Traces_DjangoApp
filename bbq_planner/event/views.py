from django.shortcuts import render
from django.contrib.auth.models import User as AuthUser
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.db import IntegrityError, transaction

from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import permissions, status, authentication


class EventResources(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @transaction.atomic
    def post(self, request):
        user = request.user

        return Response({'success': f" event is successfully created"},
                        status=status.HTTP_200_OK)
