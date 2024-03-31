from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django.contrib.sessions.models import Session
admin.site.register(CustomUser, UserAdmin)
admin.site.register(Session)