from django import forms
from user.models import UserProfile
from django.contrib.auth.models import User as DefaultUser


class UserExtendForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['city', 'phone']


class UserAuthForm(forms.ModelForm):
    class Meta:
        model = DefaultUser
        fields = ['username', 'password', 'email', 'first_name', 'last_name']


def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['password'].widget.attrs['class'] = 'form-control'
