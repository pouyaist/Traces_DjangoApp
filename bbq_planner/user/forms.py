from django import forms
from user.models import UserProfile, Attendee
from django.contrib.auth.models import User


class UserExtendForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['city', 'phone']


class UserAuthForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']


class AttendeeForm(forms.ModelForm):
    class Meta:
        model = Attendee
        fields = ['first_name', 'last_name']


def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['password'].widget.attrs['class'] = 'form-control'
