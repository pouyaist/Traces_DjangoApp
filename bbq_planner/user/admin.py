from django.contrib import admin
from user.models import UserProfile, Attendee


class UserProfileAdmin(admin.ModelAdmin):
    model = UserProfile
    list_display = ['id', 'username', 'first_name',
        'last_name', 'email', 'city', 'phone']
    search_fields = ['user_auth__username', 'user_auth__first_name',
        'user_auth__last_name', 'user_auth__email', 'city', 'phone']

    def Id(self, obj):
        return obj.user_auth.id

    def first_name(self, obj):
        return obj.user_auth.first_name

    def last_name(self, obj):
        return obj.user_auth.last_name

    def username(self, obj):
        return obj.user_auth.username

    def  email(self, obj):
        return obj.user_auth.email


class AttendeeAdmin(admin.ModelAdmin):
    model = Attendee
    list_display = ['id', 'first_name', 'last_name']

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Attendee, AttendeeAdmin)
