from django.shortcuts import render
from django.contrib.auth.models import User as AuthUser
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect

from user.forms import UserAuthForm, UserExtendForm


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
