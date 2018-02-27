from django.db import models
from django.contrib.auth.models import User



class UserProfile(models.Model):
    user_auth = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=200, blank = True)
    is_admin = models.BooleanField(default=False)
    phone = models.CharField(max_length=20, default = None, blank = True)

    class Meta:
        db_table = 'user_profiles'
